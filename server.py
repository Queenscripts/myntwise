from flask import Flask, render_template, jsonify, flash, session, redirect, request
from model import connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
import crud
import json
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

SESSION_TYPE = 'filesystem'

app.secret_key = 'ABCSECRETDEF'


@app.route('/')
def homepage(): 
    """"Show homepage"""
    categories = crud.get_categories()
    # print(session['user_email'], 'SESSO')
    # if session and session['user_email']:
    #     user = session['user_email']
    #     return render_template('home.html', user=user, categories=categories)
    return render_template('home.html', categories=categories)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    """Show dashboard"""
    return render_template('dashboard.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Show signup page"""
    if request.method == "POST": 
        # Query user name to make sure not already taken 
        email = request.form.get('email').strip()
        password = request.form.get('password')
        hashed_pass = generate_password_hash(password)

        
        user_in_db = crud.get_user_by_email(email)


        if user_in_db: 
            return render_template('login.html', email=user_in_db)
        if not email: 
            flash("Must include email")
        if not password: 
            flash("Must provide password")

        else: 
            new_user = crud.create_user(email, hashed_pass)
            # print(new_user, 'NEW USER')

            db.session.add(new_user)
            db.session.commit()

        session['user_email']= email
        print('SESSION', session)
        return redirect('/')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    """ Login User """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = crud.get_user_by_email(email)
        if not user:
            flash('Invalid') 
        else: 
            flash('valid') 
            session["user_email"] = user.email
        return redirect("/")
    if request.method == 'GET':
        return render_template("login.html") 

@app.route('/logout', methods=['GET'])
def logout(): 
    """ Logout User """
    session.clear()
    return redirect("/dashboard")

@app.route('/budgets', methods=['GET', 'POST', 'PUT', 'DELETE'])
def budgets():
    """Show budgets page"""
    budgets = crud.get_budgets()
    if request.method == "GET": 
    #     # Query user name to make sure not already taken 
    #     email = request.form.get('email').strip()
        return render_template('budget.html', budgets = budgets)
    if request.method == "POST":
        budget_name = request.form.get('budget_name')
        budget_amount = request.form.get('budget_amount')
        budget_description = request.form.get('budget_description')
        budget_frequency = request.form.get('budget_frequency')


# API ROUTES 

@app.route('/api/all-users')
def display_users():
    """Show users"""
    users = crud.get_users()
    print(users, 'USERS')
    
    # return jsonify(users)
    usery=[]
    for user in users:
        userz={} 
        
        userz["email"]=str(user.email)
        userz["user_id"]=str(user.user_id)
        usery.append(userz)
    print(usery)
    return jsonify(usery)

@app.route('/api/all-budgets')
def display_budgets():
    """Show budgets"""
    budgets = crud.get_budgets()
    
    # return jsonify(users)
    budgetlist=[]
    for budget in budgets:
        budget_item={} 
        budget_item["user_id"]=str(budget.user_id)
        budget_item["budget_name"]=str(budget.budget_name)
        budget_item["budget_id"]=str(budget.budget_id)
        budget_item["budget_description"]=str(budget.budget_description)
        budget_item["budget_frequency"]=str(budget.budget_frequency)
        budgetlist.append(budget_item)
        print(budget)
    print(budgets)
    return jsonify(budgetlist)

if __name__ == "__main__": 
    app.debug = False 
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.config.from_object(__name__)

    app.run(host="0.0.0.0")