from flask import Flask, render_template, request
from forms import PlayerSelectionForm


# WebApp configuration and file paths
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ao19s2en1638nsh6msh172kd0s72ksj2'


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
