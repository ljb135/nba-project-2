from flask import Flask, render_template, request, jsonify, flash
from forms import PlayerSelectionForm
from sqlalchemy import create_engine, select, and_
import numpy as np
import pickle
from team import Team
from players_schema import Players_Table

# WebApp configuration and file paths
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ao19s2en1638nsh6msh172kd0s72ksj2'

db = create_engine('sqlite:///NBAPlayers.db', echo=False)
players_table = Players_Table.__table__

Pkl_Filename = "ML_Models/models/NBA_RFModel.pkl"
with open(Pkl_Filename, 'rb') as file:
    model = pickle.load(file)


# Executes queries - returns dictionaries of home and away player stats
def get_stats(season, home_players, away_players):
    query = select([players_table]).where(
        and_(players_table.c.SEASON == season, players_table.c.PLAYER_ID.in_(home_players)))
    conn = db.connect()
    result = conn.execute(query)
    home_stats = [dict(r) for r in result]

    query = select([players_table]).where(
        and_(players_table.c.SEASON == season, players_table.c.PLAYER_ID.in_(away_players)))
    conn = db.connect()
    result = conn.execute(query)
    away_stats = [dict(r) for r in result]

    return home_stats, away_stats


# Processes information entered into form - returns an array of stats to be analyzed by our model
def stats_mod(season, home_players, away_players):
    home_stats, away_stats = get_stats(season, home_players, away_players)

    game_data_array = []
    adjust_for_minutes(home_stats, 240)
    adjust_for_minutes(away_stats, 240)

    game_data_array.extend(Team(home_stats).export())
    game_data_array.extend(Team(away_stats).export())

    return np.array(game_data_array)


def adjust_for_minutes(players, rem_min):
    overflow = False
    edit_stat_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24]

    total_min = 0
    for player in players:
        total_min += player[0]
    min_ratio = rem_min / total_min

    adj_players = []
    not_adj_players = []
    for player in players:
        if player[0] * min_ratio > 40:
            min_ratio = 40 / player[0]
            for index in edit_stat_indexes:
                player[index] = player[index] * min_ratio
            overflow = True
            adj_players.append(player)
        else:
            not_adj_players.append(player)

    if not overflow:
        for player in players:
            for index in edit_stat_indexes:
                player[index] = player[index] * min_ratio
    else:
        adj_min = 0
        for player in adj_players:
            adj_min += player[0]
        adjust_for_minutes(not_adj_players, rem_min - adj_min)


# Route for webapp homepage - contains form
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', title='Home')


# Route for form page
@app.route('/form', methods=('GET', 'POST'))
def form_page():
    form = PlayerSelectionForm()

    if request.method == "POST" and form.validate():
        season = form.season.data
        home_players = [row["player"] for row in form.home_players.data]
        away_players = [row["player"] for row in form.away_players.data]

        stats = np.array([stats_mod(season, home_players, away_players)])
        print("Home: ", stats[0][0:20])
        print("Away: ", stats[0][20:])
        prediction = model.predict_proba(stats)
        message = "The probability that the home team wins is " + str((prediction[0][1] * 100).round(1)) + "%"
        flash(message)

    return render_template('form.html', title='Form', form=form)


# Route for about us page
@app.route('/about')
def about_page():
    return render_template('about.html', title='About Us')


# Queries database for list of names given the year - returns a JSON dictionary of objects containing player name and ID
@app.route('/playerlist/<year>')
def playerlist(year):
    query = select([players_table.c.PLAYER_ID, players_table.c.TEAM_ABBREVIATION, players_table.c.PLAYER_NAME]).where(
        players_table.c.SEASON == year)
    conn = db.connect()
    result = conn.execute(query)

    player_array = []

    for player in result:
        playerObj = {}
        playerObj["name"] = player.PLAYER_NAME + ", " + player.TEAM_ABBREVIATION
        playerObj["playerID"] = player.PLAYER_ID
        player_array.append(playerObj)

    return jsonify({"players": player_array})


# Queries database for list of teams given the year - returns a JSON dictionary of objects containing team name and ID
@app.route('/teamlist/<year>')
def teamlist(year):
    query = select([players_table.c.TEAM_ID, players_table.c.TEAM_NAME]).where(
        players_table.c.SEASON == year).distinct().order_by(
        players_table.c.TEAM_NAME)
    conn = db.connect()
    result = conn.execute(query)

    team_array = []

    for team in result:
        teamObj = {}
        teamObj["name"] = team.TEAM_NAME
        teamObj["teamID"] = team.TEAM_ID
        team_array.append(teamObj)

    return jsonify({"teams": team_array})


# Queries database for list of names given the team and year - returns a JSON dictionary of objects containing player name and ID
@app.route('/autofill/<year>/<team_id>')
def autofill(year, team_id):
    query = select([players_table.c.PLAYER_ID, players_table.c.TEAM_ABBREVIATION, players_table.c.PLAYER_NAME]).where(
        and_(players_table.c.SEASON == year, players_table.c.TEAM_ID == team_id,
             players_table.c.MIN * players_table.c.GP > 100)).order_by(
        (players_table.c.MIN).desc()).limit(8)
    conn = db.connect()
    result = conn.execute(query)

    player_array = []

    for player in result:
        playerObj = {}
        playerObj["name"] = player.PLAYER_NAME + ", " + player.TEAM_ABBREVIATION
        playerObj["playerID"] = player.PLAYER_ID
        player_array.append(playerObj)

    return jsonify({"players": player_array})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
