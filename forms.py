from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, Form, FormField, FieldList
from wtforms.validators import InputRequired


# Form for a single player to be duplicated in PlayerSelectionForm
class PlayerForm(Form):
    player = SelectField('Player', validators=[InputRequired()], choices=[])


# User entry form for entering players on home/away teams
class PlayerSelectionForm(FlaskForm):
    year_options = [("Select", "Select")]
    for i in range(2015, 2020):
        year_options.append((str(i), f"{i}-{i + 1}"))

    season = SelectField('Season', validators=[InputRequired()], choices=year_options)
    home_team = SelectField('Home_Team', choices=["Select"])
    away_team = SelectField('Away_Team', choices=["Select"])
    home_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)
    away_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)

    submit = SubmitField('Predict!')
