from flask import Flask, render_template


# WebApp configuration and file paths
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ao19s2en1638nsh6msh172kd0s72ksj2'


# Route for webapp homepage - contains form
@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def homepage():
    return render_template('requestBS.html', title='Home')


# Route for about us page
@app.route('/about')
def about_page():
    return render_template('about.html', title='About Us')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
