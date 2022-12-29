from flask import Flask, render_template, request, jsonify, flash
from forms import PlayerSelectionForm
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_
import numpy as np
import pickle
from Team import Team

# WebApp configuration and file paths
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ao19s2en1638nsh6msh172kd0s72ksj2'
db = create_engine('sqlite:///NBAPlayers.db', echo=False)
meta = MetaData()
Pkl_Filename = "ML_Models/models/NBA_RFModel.pkl"
with open(Pkl_Filename, 'rb') as file:
    model = pickle.load(file)

# Table format from database
players = Table('v_players2', meta,
                Column('NAME', String),
                Column('PLAYER_ID', String, primary_key=True),
                Column('TEAM_ABR', String),
                Column('TEAM_ID', String),
                Column('YEAR', String, primary_key=True),
                Column('AGE', Integer),
                Column('HEIGHT', Integer),
                Column('WEIGHT', Integer),
                Column('GP', Integer),
                Column('MIN', Integer),
                Column('PTS', Integer),
                Column('FTM', Integer),
                Column('FTA', Integer),
                Column('FT_PCT', Integer),
                Column('FGM', Integer),
                Column('FGA', Integer),
                Column('FG_PCT', Integer),
                Column('FG3M', Integer),
                Column('FG3A', Integer),
                Column('FG3_PCT', Integer),
                Column('AST', Integer),
                Column('TOV', Integer),
                Column('STL', Integer),
                Column('BLK', Integer),
                Column('OREB', Integer),
                Column('DREB', Integer),
                Column('PF', Integer),
                Column('OFF_RTG', Integer),
                Column('DEF_RTG', Integer),
                Column('DEFL', Integer),
                Column('LB_REC', Integer),
                Column('CONT_2P', Integer),
                Column('CONT_3P', Integer),
                Column('DFG2M', Integer),
                Column('DFG2A', Integer),
                Column('DFG3M', Integer),
                Column('DFG3A', Integer),
                Column('INJ', Integer),
                Column('TEAM_NAME', String))


# Processes information entered into form - returns an array of stats to be analyzed by our model
def get_stats(season, home_players, away_players):
    home_stats = []
    for player in home_players:
        player_id = player["player"]
        if player_id != "Select":
            query = select([players]).where(and_(players.c.YEAR == season, players.c.PLAYER_ID == player_id))
            conn = db.connect()
            result = conn.execute(query)

            result = result.fetchone().values()
            delete_indexes = [13, 16, 19, 37, 38]
            for index in sorted(delete_indexes, reverse=True):
                del result[index]
            del result[:9]
            home_stats.append(result)

    away_stats = []
    for player in away_players:
        player_id = player["player"]
        if player_id != "Select":
            query = select([players]).where(and_(players.c.YEAR == season, players.c.PLAYER_ID == player_id))
            conn = db.connect()
            result = conn.execute(query)

            result = result.fetchone().values()
            delete_indexes = [13, 16, 19, 37, 38]
            for index in sorted(delete_indexes, reverse=True):
                del result[index]
            del result[:9]
            away_stats.append(result)

    return np.array(stats_mod(home_stats, away_stats))


def stats_mod(home_players, away_players):
    game_data_array = []
    calc_stats(home_players, 240)
    calc_stats(away_players, 240)

    game_data_array.extend(Team(home_players).export())
    game_data_array.extend(Team(away_players).export())

    return game_data_array


def calc_stats(players, rem_min):
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
        calc_stats(not_adj_players, rem_min - adj_min)


# Route for webapp homepage - contains form
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('homeBS.html', title='Home')


# Route for form page
@app.route('/form', methods=('GET', 'POST'))
def form_page():
    form = PlayerSelectionForm()

    if request.method == "POST" and form.validate_on_submit():
        season = form.season.data
        home_players = form.home_players.data
        away_players = form.away_players.data

        stats = np.array([get_stats(season, home_players, away_players)])
        print("Home: ", stats[0][0:20])
        print("Away: ", stats[0][20:])
        prediction = model.predict_proba(stats)
        message = "The probability that the home team wins is " + str((prediction[0][1] * 100).round(1)) + "%"
        flash(message)

    return render_template('formBS.html', title='Form', form=form)


# Route for background page
# @app.route('/model')
# def model_page():
#     return render_template('modelBS.html', title='Our Model')


# Route for about us page
@app.route('/about')
def about_page():
    return render_template('aboutBS.html', title='About Us')


# Queries database for list of names given the year - returns a JSON dictionary of objects containing player name and ID
@app.route('/playerlist/<year>')
def playerlist(year):
    query = select([players.c.PLAYER_ID, players.c.TEAM_ABR, players.c.NAME]).where(players.c.YEAR == year)
    conn = db.connect()
    result = conn.execute(query)

    player_array = []

    for player in result:
        playerObj = {}
        playerObj["name"] = player.NAME + ", " + player.TEAM_ABR
        playerObj["playerID"] = player.PLAYER_ID
        player_array.append(playerObj)

    return jsonify({"players": player_array})


# Queries database for list of teams given the year - returns a JSON dictionary of objects containing team name and ID
@app.route('/teamlist/<year>')
def teamlist(year):
    query = select([players.c.TEAM_ID, players.c.TEAM_NAME]).where(players.c.YEAR == year).distinct().order_by(
        players.c.TEAM_NAME)
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
    query = select([players.c.PLAYER_ID, players.c.TEAM_ABR, players.c.NAME]).where(
        and_(players.c.YEAR == year, players.c.TEAM_ID == team_id, players.c.GP > 30, players.c.INJ == 0)).order_by(
        (players.c.MIN).desc()).limit(8)
    conn = db.connect()
    result = conn.execute(query)

    player_array = []

    for player in result:
        playerObj = {}
        playerObj["name"] = player.NAME + ", " + player.TEAM_ABR
        playerObj["playerID"] = player.PLAYER_ID
        player_array.append(playerObj)

    return jsonify({"players": player_array})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
