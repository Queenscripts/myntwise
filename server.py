from flask import Flask, render_template, jsonify, flash, session, redirect, request
from model import connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
import crud
import json
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from celerydb import create_celery_app
import services

app = Flask(__name__)

SESSION_TYPE = "filesystem"

app.secret_key = "ABCSECRETDEF"


# CLIENT ROUTES
@app.route("/")
def homepage():
    """"Show homepage"""
    # get_products().delay()
    categories = crud.get_categories()
    advice = crud.get_advice()
    if session and session["user_email"]:
        user = session["user_email"]
        return render_template("home.html", user=user, categories=categories)
    return render_template("home.html", advice=advice, categories=categories)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    """Show dashboard"""
    if session and session["user_email"]:
        user = crud.get_user_by_email(session["user_email"])
        user_budgets = crud.get_user_budgets(user.user_id)
        budget_count = crud.get_budgets_count(user.user_id)
        transaction_count = crud.get_transactions_count(user.user_id)
        categories_count = crud.get_categories_count(user.user_id)
        categories = crud.get_categories()
        transactions = crud.get_user_transactions(user.user_id)
        return render_template("dashboard.html", transactions = transactions,budgets=user_budgets, categories=categories, transaction_count=transaction_count, budget_count=budget_count, categories_count=categories_count)
    return render_template("dashboard.html")

# USER ROUTES
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Show signup page"""
    if request.method == "POST": 
        # Query user name to make sure not already taken 
        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password")
        hashed_pass = generate_password_hash(password)

        
        user_in_db = crud.get_user_by_email(email)


        if user_in_db: 
            return render_template("login.html", email=user_in_db)
        if not name:
            flash("Must include name")
        if not email: 
            flash("Must include email")
        if not password: 
            flash("Must provide password")

        else: 
            new_user = crud.create_user(name,email, hashed_pass)
            # print(new_user, "NEW USER")

            db.session.add(new_user)
            db.session.commit()

        session["user_email"]= new_user.email
        print("SESSION", session)
        return redirect("/")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login(): 
    """ Login User """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = crud.get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            flash("Invalid") 
            return redirect("/login")
        else: 
            flash("valid") 
            session["user_email"] = user.email
            return redirect("/")
    if request.method == "GET":
        return render_template("login.html") 

@app.route("/logout", methods=["GET"])
def logout(): 
    """ Logout User """
    session.clear()
    return redirect("/")

# BUDGET ROUTE
@app.route("/budgets", methods=["GET", "POST", "PUT"])
def budgets():
    """Show budgets page"""
    
    categories = crud.get_categories()
    

    if request.method == "GET":
        if session and session["user_email"]:
            user = crud.get_user_by_email(session["user_email"])
            user_budgets = crud.get_user_budgets(user.user_id)
            return render_template("budget.html", budgets = user_budgets, categories=categories)
        return render_template("budget.html", categories=categories)

    if request.method == "POST":
        user = crud.get_user_by_email(session["user_email"])
        budget_name = request.form.get("budget_name")
        budget_amount = request.form.get("budget_amount")
        budget_description = request.form.get("budget_description")
        budget_frequency = request.form.get("budget_frequency")
        category = crud.get_category(request.form.get("category"))
        

        new_budget = crud.create_budget(budget_name,budget_amount,budget_description,budget_frequency, user.user_id, category.category_id)

        db.session.add(new_budget)
        db.session.commit()
        flash(f"New budget: {new_budget.budget_name}")
        return redirect("/budgets")

@app.route("/budget/<id>", methods=["GET"])
def delete_budget(id):
    """Route to delete budget"""
    crud.delete_budget(id)
    db.session.commit()
    return redirect("/budgets")
# USER TRANSACTION ROUTES
@app.route("/transactions", methods=["GET", "POST", "PUT", "DELETE"])
def transactions():
    """Show & Handle User Transactions"""
    user = crud.get_user_by_email(session["user_email"])
    transactions = crud.get_user_transactions(user.user_id)
    categories = crud.get_categories()

    print('TRANSACTIONS', transactions)
    if request.method == "GET": 
        
        parsed_transactions = []
        for transaction in transactions:
            transaction_item={} 
            transaction_item["user_id"]=str(transaction.user_id)
            transaction_item["transaction_name"]=str(transaction.user_transactions_name)
            transaction_item["transaction_id"]=str(transaction.user_transactions_id)
            transaction_item["transaction_amount"]=str(transaction.user_transactions_amount)
            transaction_item["transaction_date"]=str(transaction.user_transactions_date)
            parsed_transactions.append(transaction_item)
        return jsonify(parsed_transactions)
    if request.method == "POST":
        user_transaction_name = request.form.get("user_transaction_name")
        user_transaction_amount = request.form.get("user_transaction_amount")
        user_transaction_date = request.form.get("user_transaction_date")
        budget = crud.get_budget_by_name(request.form.get("budget"))
        category = crud.get_category(request.form.get("category"))
        

        new_user_transaction = crud.create_user_transaction(user_transaction_name,user_transaction_amount, user_transaction_date,budget.budget_id,category.category_id, user.user_id)

        db.session.add(new_user_transaction)
        db.session.commit()
        flash(f"New user_transaction: {new_user_transaction.user_transactions_name}")
        return redirect("/transactions")


# ADVICE ROUTE
@app.route("/advice", methods=["GET", "POST", "PUT", "DELETE"])
def advice():
    """Show budgeting advice via links of place to shop online by category"""
    advice = crud.get_advice()
    query = request.args.get('query')
    # db_advice= crud.create_advice()
    if request.method == "GET": 
        
    #     # Query user name to make sure not already taken 
    #     email = request.form.get("email").strip()
        categories = crud.get_categories()

        return render_template("budget.html", budgets = budgets, categories=categories)
    if request.method == "POST":
        budget_name = request.form.get("budget_name")
        budget_amount = request.form.get("budget_amount")
        budget_description = request.form.get("budget_description")
        budget_frequency = request.form.get("budget_frequency")
        user = crud.get_user_by_email(session["user_email"])
        category = crud.get_category(request.form.get("category"))
        
        user = crud.get_user_by_email(session["user_email"])
        user_id = user.user_id

        new_budget = crud.create_budget(budget_name,budget_amount,budget_description,budget_frequency, user.user_id, category.category_id)

        db.session.add(new_budget)
        db.session.commit()
        flash(f"New budget: {new_budget.budget_name}")
        return redirect("/budgets")



# API ROUTES 
@app.route("/api/all-users")
def display_users():
    """Show users"""
    users = crud.get_users()
    print(users, "USERS")
    
    # return jsonify(users)
    usery=[]
    for user in users:
        userz={} 
        
        userz["email"]=str(user.email)
        userz["user_id"]=str(user.user_id)
        usery.append(userz)
    print(usery)
    return jsonify(usery)

@app.route("/api/all-budgets")
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
    celery=create_celery_app(app)
    @celery.task()
    def get_products(): 
        product_instance=services.ProductFeed()
        db.session.add(product_instance.fetch())
        db.session.commit()
        return "work"
    app.run(host="0.0.0.0")