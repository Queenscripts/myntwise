from flask import Flask, render_template 
from model import connect_to_db
import os
from flask_debugtoolbar import DebugToolbarExtension

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


if __name__ == "__main__": 
    app.debug = True 
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")