from flask_wtf import FlaskForm
from wtforms import SelectField, Form, FormField, FieldList
from wtforms.validators import NoneOf
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_
db = create_engine('sqlite:///NBAPlayers.db', echo=False)
meta = MetaData()

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


def playerlist():
    query = select([players.c.PLAYER_ID, players.c.TEAM_ABR, players.c.NAME]).where(players.c.YEAR == '2021')
    conn = db.connect()
    result = conn.execute(query)

    player_array = [("Default", "Select Player")]
    for player in result:
        player_array.append((player.PLAYER_ID, player.NAME + ", " + player.TEAM_ABR))
    return player_array


def teamlist():
    query = select([players.c.TEAM_ID, players.c.TEAM_NAME]).where(players.c.YEAR == '2021').distinct().order_by(
        players.c.TEAM_NAME)
    conn = db.connect()
    result = conn.execute(query)

    team_array = [("Default", "Custom")]
    for team in result:
        team_array.append((team.TEAM_ID, team.TEAM_NAME))
    return team_array


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


# Form for a single player to be duplicated in PlayerSelectionForm
class PlayerForm(Form):
    player_options = playerlist()
    player = NonValidatingSelectField('Player', validators=[NoneOf(values=["Default"], message="Please select a player.")], choices=player_options, default="Default")


# User entry form for entering players on home/away teams
class PlayerSelectionForm(FlaskForm):
    year_options = []
    for i in range(2017, 2022):
        year_options.append((str(i), f"{i - 1}-{i}"))

    team_options = teamlist()

    season = NonValidatingSelectField('Season', choices=year_options, default="2021")
    home_team = NonValidatingSelectField('Home_Team', choices=team_options, default="Default")
    away_team = NonValidatingSelectField('Away_Team', choices=team_options, default="Default")
    home_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)
    away_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)
