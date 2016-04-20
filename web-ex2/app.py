# import the Flask class from the flask module
from flask import Flask, request, render_template, make_response, redirect, url_for, session, flash,jsonify, abort
from functools import wraps

# create the application object
app = Flask(__name__)

app.secret_key = 'my precious'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decoratiots th link the function to a url
@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template('index.html') #return a string

@app.route('/welcome')
# @login_required
def welcome():
    return render_template('welcome.html', name="hi") #render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home')) 
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

@app.errorhandler(404)
def page_no_found(e):
    return jsonify(Error='Page No Found', status=404)

# start the sever with run()
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8080)
    # setting host='0.0.0.0' and port=8080 running on cloud9

