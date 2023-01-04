from flask_wtf import FlaskForm
from wtforms import SelectField, Form, FormField, FieldList
from wtforms.validators import NoneOf
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_
from datetime import date
db = create_engine('sqlite:///NBAPlayers.db', echo=False)
meta = MetaData()

# Table format from database
players = Table('v_players3', meta,
                 Column('PLAYER_NAME', String),
                 Column('PLAYER_ID', String, primary_key=True),
                 Column('TEAM_NAME', String),
                 Column('TEAM_ID', String),
                 Column('TEAM_ABBREVIATION', String),
                 Column('SEASON', String, primary_key=True),
                 Column('AGE', Integer),
                 Column('PLAYER_HEIGHT_INCHES', Integer),
                 Column('PLAYER_WEIGHT', Integer),
                 Column('DRAFT_YEAR', String),
                 Column('DRAFT_ROUND', Integer),
                 Column('DRAFT_NUMBER', Integer),
                 Column('GP', Integer),
                 Column('MIN', Integer),
                 Column('PTS', Integer),
                 Column('EFG_PCT', Integer),
                 Column('TS_PCT', Integer),
                 Column('FGM', Integer),
                 Column('FGA', Integer),
                 Column('FG_PCT', Integer),
                 Column('FG3M', Integer),
                 Column('FG3A', Integer),
                 Column('FG3_PCT', Integer),
                 Column('FTM', Integer),
                 Column('FTA', Integer),
                 Column('FT_PCT', Integer),
                 Column('OREB', Integer),
                 Column('DREB', Integer),
                 Column('REB', Integer),
                 Column('AST', Integer),
                 Column('TOV', Integer),
                 Column('STL', Integer),
                 Column('BLK', Integer),
                 Column('PF', Integer),
                 Column('PFD', Integer),
                 Column('PLUS_MINUS', Integer),
                 Column('OFF_RATING', Integer),
                 Column('DEF_RATING', Integer),
                 Column('NET_RATING', Integer),
                 Column('AST_PCT', Integer),
                 Column('AST_TO', Integer),
                 Column('AST_RATIO', Integer),
                 Column('OREB_PCT', Integer),
                 Column('DREB_PCT', Integer),
                 Column('REB_PCT', Integer),
                 Column('USG_PCT', Integer),
                 Column('PACE', Integer),
                 Column('PIE', Integer),
                 Column('POSS', Integer),
                 Column('DEFLECTIONS', Integer),
                 Column('CHARGES_DRAWN', Integer),
                 Column('SCREEN_ASSISTS', Integer),
                 Column('PTS_OFF_TOV', Integer),
                 Column('PTS_2ND_CHANCE', Integer),
                 Column('PTS_FB', Integer),
                 Column('PTS_PAINT', Integer),
                 Column('OPP_PTS_OFF_TOV', Integer),
                 Column('OPP_PTS_2ND_CHANCE', Integer),
                 Column('OPP_PTS_FB', Integer),
                 Column('OPP_PTS_PAINT', Integer),
                 Column('OPP_FGM', Integer),
                 Column('OPP_FGA', Integer),
                 Column('OPP_FG_PCT', Integer),
                 Column('OPP_FG3M', Integer),
                 Column('OPP_FG3A', Integer),
                 Column('OPP_FG3_PCT', Integer))

def playerlist():
    query = select([players.c.PLAYER_ID, players.c.TEAM_ABBREVIATION, players.c.PLAYER_NAME]).where(players.c.SEASON == f'{date.today().year}')
    conn = db.connect()
    result = conn.execute(query)

    player_array = [("Default", "Select Player")]
    for player in result:
        player_array.append((player.PLAYER_ID, player.PLAYER_NAME + ", " + player.TEAM_ABBREVIATION))
    return player_array


def teamlist():
    query = select([players.c.TEAM_ID, players.c.TEAM_NAME]).where(players.c.SEASON == f'{date.today().year}').distinct().order_by(
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
    player = SelectField('Player', validators=[NoneOf(values=["Default"], message="Please select a player.")], choices=player_options, default="Default")


# User entry form for entering players on home/away teams
class PlayerSelectionForm(FlaskForm):
    year_options = []

    current_year = date.today().year

    # Set default to current year to ensure enough data is collected for each season
    # if date.today().month >= 10:
    #     current_year += 1

    # Only updates year field for calendar new year
    for i in range(2017, current_year + 1):
        year_options.append((str(i), f"{i - 1}-{i}"))

    team_options = teamlist()

    season = SelectField('Season', choices=year_options, default=f"{current_year}")
    home_team = SelectField('Home_Team', choices=team_options, default="Default")
    away_team = SelectField('Away_Team', choices=team_options, default="Default")
    home_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)
    away_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)
