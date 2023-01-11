from flask_wtf import FlaskForm
from wtforms import SelectField, Form, FormField, FieldList
from wtforms.validators import NoneOf, Required
from sqlalchemy import create_engine, select
from datetime import date
from v_players_schema import Players_Table

db = create_engine('sqlite:///NBAPlayers.db', echo=False)
players_table = Players_Table.__table__

def playerlist():
    query = select([players_table.c.PLAYER_ID, players_table.c.TEAM_ABBREVIATION, players_table.c.PLAYER_NAME]).where(players_table.c.SEASON == f'{date.today().year}')
    conn = db.connect()
    result = conn.execute(query)

    player_array = [("Default", "Select Player")]
    for player in result:
        player_array.append((player.PLAYER_ID, player.PLAYER_NAME + ", " + player.TEAM_ABBREVIATION))
    return player_array


def teamlist():
    query = select([players_table.c.TEAM_ID, players_table.c.TEAM_NAME]).where(players_table.c.SEASON == f'{date.today().year}').distinct().order_by(
        players_table.c.TEAM_NAME)
    conn = db.connect()
    result = conn.execute(query)

    team_array = [("Default", "Custom")]
    for team in result:
        team_array.append((team.TEAM_ID, team.TEAM_NAME))
    return team_array


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
    home_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8, validators=[Required()])
    away_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8, validators=[Required()])
