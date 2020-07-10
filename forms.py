from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, Form, FormField, FieldList
from wtforms.validators import InputRequired, Length


# Form for a single player to be duplicated in PlayerSelectionForm
class PlayerForm(Form):
    year_options = [("Empty", "Empty")]
    for i in range(1996, 2020):
        year_options.append((str(i), f"{i}-{i + 1}"))

    year = SelectField('Year', validators=[InputRequired()], choices=year_options)
    player_name = SelectField('Player Name', validators=[InputRequired()], choices=[])


# User entry form for entering players on home/away teams
class PlayerSelectionForm(FlaskForm):
    home_players = FieldList(FormField(PlayerForm), min_entries=13, max_entries=13)
    away_players = FieldList(FormField(PlayerForm), min_entries=13, max_entries=13)

    submit = SubmitField('Predict!')
