from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, Form, FormField, FieldList
from wtforms.validators import InputRequired


# Form for a single player to be duplicated in PlayerSelectionForm
class PlayerForm(Form):
    player = SelectField('Player', validators=[InputRequired()], choices=[])


# User entry form for entering players on home/away teams
class PlayerSelectionForm(FlaskForm):
    year_options = [("Default", "Select Season")]
    for i in range(2015, 2020):
        year_options.append((str(i), f"{i}-{i + 1}"))

    season = SelectField('Season', validators=[InputRequired()], choices=year_options, default=2020)
    home_team = SelectField('Home_Team', choices=[("Default", "No Team Selected")])
    away_team = SelectField('Away_Team', choices=[("Default", "No Team Selected")])
    home_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)
    away_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)