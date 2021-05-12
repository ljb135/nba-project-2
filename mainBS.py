from flask import Flask, render_template

# WebApp configuration and file paths
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ao19s2en1638nsh6msh172kd0s72ksj2'


# Route for webapp homepage - contains form
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('homeBS.html', title='Home')


# Route for about us page
@app.route('/about')
def about_page():
    return render_template('aboutBS.html', title='About Us')


# Route for form page
@app.route('/form', methods=('GET', 'POST'))
def form_page():
    return render_template('formBS.html', title='Form')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
