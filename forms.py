from flask_wtf import FlaskForm
from wtforms import SelectField, Form, FormField, FieldList
from wtforms.validators import InputRequired, NoneOf


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


# Form for a single player to be duplicated in PlayerSelectionForm
class PlayerForm(Form):
    player = NonValidatingSelectField('Player', validators=[NoneOf(values=["Default"], message="Please select a player.")], choices=[])


# User entry form for entering players on home/away teams
class PlayerSelectionForm(FlaskForm):
    year_options = [("Default", "Select Season")]
    for i in range(2017, 2022):
        year_options.append((str(i), f"{i - 1}-{i}"))

    season = NonValidatingSelectField('Season', choices=year_options)
    home_team = NonValidatingSelectField('Home_Team', choices=[("Default", "No Team Selected")])
    away_team = NonValidatingSelectField('Away_Team', choices=[("Default", "No Team Selected")])
    home_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)
    away_players = FieldList(FormField(PlayerForm), min_entries=8, max_entries=8)