from flask import Flask, render_template, request, jsonify
from forms import PlayerSelectionForm
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_
import numpy as np
import pickle

# WebApp configuration and file paths
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ao19s2en1638nsh6msh172kd0s72ksj2'
db = create_engine('sqlite:///NBAPlayers.db', echo=False)
meta = MetaData()
Pkl_Filename = "NBA_LRModel.pkl"
with open(Pkl_Filename, 'rb') as file:
    model = pickle.load(file)

# Table format from database
players = Table('v_players', meta,
                Column('NAME', String),
                Column('PLAYER_ID', String, primary_key=True),
                Column('TEAM', String),
                Column('TEAM_ID', String),
                Column('YEAR', String, primary_key=True),
                Column('AGE', Integer),
                Column('HEIGHT', Integer),
                Column('WEIGHT', Integer),
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
                Column('TEAM_NAME', String))


# Route for webapp homepage - contains form
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('homeBS.html', title='Home')


# Route for form page
@app.route('/form', methods=('GET', 'POST'))
def form_page():
    form = PlayerSelectionForm()

    player_choices = [("Select", "Select Player")]
    for home_player in form.home_players:
        home_player.player.choices = player_choices
    for away_player in form.away_players:
        away_player.player.choices = player_choices

    if request.method == "POST":
        season = form.season.data
        home_players = form.home_players.data
        away_players = form.away_players.data

    return render_template('formBS.html', title='Form', form=form)

# Route for background page
@app.route('/model')
def model_page():
    return render_template('modelBS.html', title='Our Model')

# Route for about us page
@app.route('/about')
def about_page():
    return render_template('aboutBS.html', title='About Us')


# Queries database for list of names given the year - returns a JSON dictionary of objects containing player name and ID
@app.route('/playerlist/<year>')
def playerlist(year):
    query = select([players.c.PLAYER_ID, players.c.TEAM, players.c.NAME]).where(players.c.YEAR == year)
    conn = db.connect()
    result = conn.execute(query)

    player_array = []

    for player in result:
        playerObj = {}
        playerObj["name"] = player.NAME + ", " + player.TEAM
        playerObj["player_id"] = player.PLAYER_ID
        player_array.append(playerObj)

    return jsonify({"players": player_array})


# Queries database for list of names given the team and year - returns a JSON dictionary of objects containing player name and ID
@app.route('/autofill/<year>/<team_id>')
def autofill(year, team_id):
    query = select([players.c.PLAYER_ID, players.c.TEAM, players.c.NAME]).where(and_(players.c.YEAR == year, players.c.TEAM_ID == team_id)).order_by(players.c.MIN.desc()).limit(8)
    conn = db.connect()
    result = conn.execute(query)

    player_array = []

    for player in result:
        playerObj = {}
        playerObj["name"] = player.NAME + ", " + player.TEAM
        playerObj["player_id"] = player.PLAYER_ID
        player_array.append(playerObj)

    return jsonify({"players": player_array})


# Queries database for list of teams given the year - returns a JSON dictionary of objects containing team name and ID
@app.route('/teamlist/<year>')
def teamlist(year):
    query = select([players.c.TEAM_ID, players.c.TEAM_NAME]).where(players.c.YEAR == year).distinct().order_by(players.c.TEAM_NAME)
    conn = db.connect()
    result = conn.execute(query)

    team_array = []

    for team in result:
        teamObj = {}
        teamObj["name"] = team.TEAM_NAME
        teamObj["team_id"] = team.TEAM_ID
        team_array.append(teamObj)

    return jsonify({"teams": team_array})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
