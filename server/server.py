from flask import Flask, render_template, jsonify
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
import crud

app = Flask(__name__)


# app.secret_key = 'ABCSECRETDEF'


@app.route('/')
def homepage(): 
    """"Show homepage"""
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    """Show dashboard"""
    return render_template('dashboard.html')

# API ROUTES 

@app.route('/api/all-users')
def display_users():
    """Show users"""
    users = crud.get_users()
    return jsonify(users)


if __name__ == "__main__": 
    app.debug = True 
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")