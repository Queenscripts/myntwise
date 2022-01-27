from unicodedata import category
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
def index(): 
    return render_template("index.html")

@app.route("/<path:path>", defaults={'path':''})
def catch_all(path): 
    return render_template("index.html")
    # return f"You want ${path}"

# def homepage():
#     """"Show homepage"""
#     query=request.args.get("query")
#     if query:
#         get_products(query).delay()
#     categories = crud.get_categories()
#     advice = crud.get_advice()
#     advice_prices=[]
#     for price in advice: 
#         advice_prices.append(price.advice_price)
#     if session and session["user_email"]:
#         user = crud.get_user_by_email(session["user_email"])
#         budgets = crud.get_user_budgets(user.user_id)
#         more_percentages =[]
#         dict_budget = []
   
#         for budget in budgets:
#             separated_list = []
#             amount = budget.budget_amount
#             budget_name = budget.budget_name
#             dict_budget.append(budget_name)
#             for price in advice: 
#                 price = price.advice_price
#                 percentage = round((price/amount)*100, 1)

#                 separated_list.append(percentage)
#                 print(price, amount, budget_name)
#             more_percentages.append(separated_list)
#         print(more_percentages)
#         advice_prices=[]
#         for price in advice: 
#             advice_prices.append(price.advice_price)
#         return render_template("home.html", prices=advice_prices, percentages = more_percentages, budgets= budgets, advice=advice, user=user, categories=categories)
#     else:
#         return render_template("public.html", prices=advice_prices, advice=advice, categories=categories)

# @app.route("/price", methods=["GET"])
# def return_custom_price_data(): 
#     if request.method== "GET":
#         categories = crud.get_categories()
#         min_price=request.args.get('min')
#         max_price=request.args.get('max')
#         results = crud.filter_advice_by_price(min_price, max_price)
#         if session and session["user_email"]:
           
#             user = crud.get_user_by_email(session["user_email"])
#             budgets = crud.get_user_budgets(user.user_id)
#             more_percentages =[]
#             dict_budget = []
#             for budget in budgets:
#                 separated_list = []
#                 amount = budget.budget_amount
#                 budget_name = budget.budget_name
#                 dict_budget.append(budget_name)
#                 for price in results: 
#                     price = price.advice_price
#                     percentage = round((price/amount)*100, 1)

#                     separated_list.append(percentage)
#                     print(price, amount, budget_name)
#                 more_percentages.append(separated_list)
#             print(more_percentages)
#             advice_prices=[]
#             for price in results: 
#                 advice_prices.append(price.advice_price)
#             return render_template("home.html", advice=results, prices=advice_prices, percentages = more_percentages, budgets= budgets, user=user, categories=categories)
#         else: 
#             return render_template("home.html", advice=results, categories=categories)

# @app.route("/category/<category_id>", methods=["GET"])    
# def return_custom_category_data(category_id):
#     if request.method== "GET":
#         # advice = crud.get_advice()
#         # category_id=request.args.get('category_id')
#         categories = crud.get_categories()
#         advice = crud.filter_advice_by_category(category_id)
#         # min_price=request.args.get('min')
#         # max_price=request.args.get('max')
#         # results = crud.filter_advice_by_price(min_price, max_price)
#         user = crud.get_user_by_email(session["user_email"])
#         budgets = crud.get_user_budgets(user.user_id)
#         more_percentages =[]
#         dict_budget = []
#         for budget in budgets:
#             separated_list = []
#             amount = budget.budget_amount
#             budget_name = budget.budget_name
#             dict_budget.append(budget_name)
#             for price in advice: 
#                 price = price.advice_price
#                 percentage = round((price/amount)*100, 1)

#                 separated_list.append(percentage)
#                 print(price, amount, budget_name)
#             more_percentages.append(separated_list)
#         print(more_percentages)
#         advice_prices=[]
#         for price in advice: 
#             advice_prices.append(price.advice_price)
#         return render_template("home.html", advice=advice, prices=advice_prices, percentages = more_percentages, budgets= budgets, user=user, categories=categories)

# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/test")
# def test():
#     return render_template("index.html")

# @app.route("/dashboard")
# def dashboard():
#     """Show dashboard"""
#     if session and session["user_email"]:
#         user = crud.get_user_by_email(session["user_email"])
#         users_advice = crud.get_advice_by_user_id(user.user_id)
#         user_budgets = crud.get_user_budgets(user.user_id)
#         budget_count = crud.get_budgets_count(user.user_id)
#         transaction_count = crud.get_transactions_count(user.user_id)
#         categories_count = crud.get_categories_count(user.user_id)
#         categories = crud.get_categories()
#         budgets = crud.get_user_budgets(user.user_id)
#         more_percentages =[]
#         transactions = crud.get_user_transactions(user.user_id)

#         saved_transactions  = crud.get_total_transaction_saved(user.user_id)
#         transactions_total= crud.get_total_sum_transactions(user.user_id)
#         saved_total = crud.get_total_transaction_saved(user.user_id)
#         print('SAVED', saved_total)
#         more_percentages =[]
#         dict_budget = []
   
#         for budget in budgets:
#             separated_list = []
#             amount = budget.budget_amount
#             budget_name = budget.budget_name
#             dict_budget.append(budget_name)
#             for price in users_advice: 
#                 price = price.advice_price
#                 percentage = round((price/amount)*100, 1)

#                 separated_list.append(percentage)
#             more_percentages.append(separated_list)
#         advice_prices=[]
#         for price in users_advice: 
#             advice_prices.append(price.advice_price)
#         saved_info = crud.get_total_transactions(user.user_id)
#         return render_template("dashboard.html", saved_info=saved_info, percentages = more_percentages, users_advice=users_advice, saved_transactions = saved_transactions, saved_total = saved_total, transactions_total=transactions_total,transactions = transactions,budgets=user_budgets, categories=categories, transaction_count=transaction_count, budget_count=budget_count, categories_count=categories_count, user=user)
#     return render_template("dashboard.html")

# # USER ROUTES
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     """Show signup page"""
#     if request.method == "POST": 
#         # Query user name to make sure not already taken 
#         name = request.form.get("name").strip()
#         email = request.form.get("email").strip()
#         password = request.form.get("password")
#         hashed_pass = generate_password_hash(password)

        
#         user_in_db = crud.get_user_by_email(email)


#         if user_in_db: 
#             return render_template("login.html", email=user_in_db)
#         if not name:
#             flash("Must include name")
#         if not email: 
#             flash("Must include email")
#         if not password: 
#             flash("Must provide password")

#         else: 
#             new_user = crud.create_user(name,email, hashed_pass)
#             # print(new_user, "NEW USER")

#             db.session.add(new_user)
#             db.session.commit()

#         session["user_email"]= new_user.email
#         return redirect("/")

#     return render_template("signup.html")

# @app.route("/login", methods=["GET", "POST"])
# def login(): 
#     """ Login User """
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")

#         user = crud.get_user_by_email(email)
#         if not user or not check_password_hash(user.password, password):
#             flash("Invalid") 
#             return redirect("/login")
#         else: 
#             flash("valid") 
#             session["user_email"] = user.email
#             return redirect("/")
#     if request.method == "GET":
#         return render_template("login.html") 

# @app.route("/logout", methods=["GET"])
# def logout(): 
#     """ Logout User """
#     session.clear()
#     return redirect("/")

# # BUDGET ROUTE
# @app.route("/budgets", methods=["GET", "POST", "PUT"])
# def budgets():
#     """Show budgets page"""
    
#     categories = crud.get_categories()
    

#     if request.method == "GET":
#         if session and session["user_email"]:
#             user = crud.get_user_by_email(session["user_email"])
#             budgets = crud.get_user_budgets(user.user_id)
#             transactions = crud.get_budgets_and_transactions(user.user_id)
#             diff = crud.get_total_transaction_amount(user.user_id)
#             # for budget in budgets:
#             #     append_budget = {}
#             #     # append_budget["category_id"],append_budget["budget_frequency"],append_budget["budget_name"],append_budget["budget_description"],append_budget["budget_amount"],append_budget["user_transactions_name"], append_budget["user_transactions_amount"], append_budget["user_transactions_date"]=budget[0].category_id,budget[0].budget_frequency,budget[0].budget_name, budget[0].budget_description, budget[0].budget_amount, budget[1].user_transactions_name, budget[1].user_transactions_amount, budget[1].user_transactions_date
#             #     transactions.append(budget[1])
#             # # print('B',user_budgets[0])
#             return render_template("budget.html", diff =diff, transactions =transactions,  budgets = budgets, categories=categories)
#         return render_template("budget.html", categories=categories)

#     if request.method == "POST":
#         user = crud.get_user_by_email(session["user_email"])
#         budget_name = request.form.get("budget_name")
#         budget_amount = request.form.get("budget_amount")
#         budget_description = request.form.get("budget_description")
#         budget_frequency = request.form.get("budget_frequency")
#         category = crud.get_category(request.form.get("category"))
        
#         new_budget = crud.create_budget(budget_name,budget_amount,budget_description,budget_frequency, user.user_id, category.category_id)

#         db.session.add(new_budget)
#         db.session.commit()
#         flash(f"New budget: {new_budget.budget_name}")
#         return redirect("/budgets")

# @app.route("/budget/<id>", methods=["GET"])
# def delete_budget(id):
#     """Route to delete budget"""
#     crud.delete_budget(id)
#     db.session.commit()
#     return redirect("/budgets")
# #@TODO Route for update

# # USER TRANSACTION ROUTES
# @app.route("/transactions", methods=["GET", "POST", "PUT", "DELETE"])
# def transactions():
#     """Show & Handle User Transactions"""
#     user = crud.get_user_by_email(session["user_email"])
#     transactions = crud.get_user_transactions(user.user_id)
#     categories = crud.get_categories()

#     if request.method == "GET": 
#         parsed_transactions = []
#         for transaction in transactions:
#             transaction_item={} 
#             transaction_item["user_id"]=str(transaction.user_id)
#             transaction_item["transaction_name"]=str(transaction.user_transactions_name)
#             transaction_item["transaction_id"]=str(transaction.user_transactions_id)
#             transaction_item["transaction_amount"]=str(transaction.user_transactions_amount)
#             transaction_item["transaction_date"]=str(transaction.user_transactions_date)
#             parsed_transactions.append(transaction_item)
#         # user_transaction_name = request.form.get("user_transaction_name")
#         # user_transaction_amount = request.form.get("user_transaction_amount")
#         # user_transaction_date = request.form.get("user_transaction_date")
        
#         # new_user_transaction = crud.create_user_transaction(user_transaction_name,user_transaction_amount, user_transaction_date,budget.budget_id,category.category_id, user.user_id)

#         # db.session.add(new_user_transaction)
#         # db.session.commit()
#         # return redirect("/home")
#         # budget = crud.get_budget_by_name(request.form.get("budget"))
#         # category = crud.get_category(request.form.get("category"))
#         # user_transaction_processed = request.args.get("user_transaction_processed")
#     if request.method == "POST":

#         request_data = request.get_json(force=True)

#         print('DATA', request_data)
#         user = crud.get_user_by_email(session["user_email"])
#         user_transactions_name = request.form.get("user_transaction_name") or request_data["user_transactions_name"]
#         user_transactions_amount = request.form.get("user_transaction_amount") or request_data["user_transactions_amount"]
#         user_transactions_date = request.form.get("user_transaction_date") or request_data["user_transactions_date"]
#         user_transactions_processed = request_data["user_transactions_processed"]
#         # if request_data and request_data["budget"] and request_data["category"]:
#         budget = crud.get_budget_by_name(request.form.get("budget")) or crud.get_budget_by_name(request_data["budget"]) or None
#         category = crud.get_category(request.form.get("category")) or crud.get_category(request_data["category"]) or None
#         if budget == None and category == None:
#             new_user_transaction = crud.create_user_transaction(user_transactions_name,user_transactions_amount, user_transactions_date, budget, category, user.user_id, user_transactions_processed)
#             db.session.add(new_user_transaction)
#             db.session.commit()
#         new_user_transaction = crud.create_user_transaction(user_transactions_name,user_transactions_amount, user_transactions_date,budget.budget_id,category.category_id, user.user_id, user_transactions_processed)
#         # else: 
#             # 
#         db.session.add(new_user_transaction)
#         db.session.commit()
#         flash(f"New user_transaction: {new_user_transaction.user_transactions_name}")
#         return redirect("/transactions")

# @app.route("/transaction/<id>", methods=["GET"])
# def delete_transaction(id):
#     """Route to delete transaction"""
#     crud.delete_transaction(id)
#     db.session.commit()
#     return redirect("/dashboard")
# # ADVICE ROUTE

# @app.route("/advice", methods=["GET", "POST", "PUT", "DELETE"])
# def advice():
#     """Show budgeting advice via links of place to shop online by category"""
#     advice = crud.get_advice()
    
#     query = request.args.get('query')
#     # db_advice= crud.create_advice()
#     if request.method == "GET": 
#         price= request.args.get('price')
#         print('PRICE', price)
#         advice_by_price = crud.get_advice_by_price(price)
#         print(advice_by_price)
#         return tuple(advice_by_price)
#     if request.method == "POST":
#         budget_name = request.form.get("budget_name")
#         budget_amount = request.form.get("budget_amount")
#         budget_description = request.form.get("budget_description")
#         budget_frequency = request.form.get("budget_frequency")
#         user = crud.get_user_by_email(session["user_email"])
#         category = crud.get_category(request.form.get("category"))
        
#         user = crud.get_user_by_email(session["user_email"])
#         user_id = user.user_id

#         new_budget = crud.create_budget(budget_name,budget_amount,budget_description,budget_frequency, user.user_id, category.category_id)

#         db.session.add(new_budget)
#         db.session.commit()
#         flash(f"New budget: {new_budget.budget_name}")
#         return redirect("/budgets")

# # API ROUTES 
# @app.route("/api/all-users")
# def display_users():
#     """Show users"""
#     users = crud.get_users()
#     print(users, "USERS")
    
#     # return jsonify(users)
#     usery=[]
#     for user in users:
#         userz={} 
        
#         userz["email"]=str(user.email)
#         userz["user_id"]=str(user.user_id)
#         usery.append(userz)
#     print(usery)
#     return jsonify(usery)

# @app.route("/api/all-budgets")
# def display_budgets():
    # """Show budgets"""
    # user=crud.get_user_by_email(session["user_email"])
    # budgets = crud.get_user_budgets(user.user_id)
    
    # # return jsonify(users)
    # budgetlist=[]
    # for budget in budgets:
    #     budget_item={} 
    #     budget_item["user_id"]=str(budget.user_id)
    #     budget_item["budget_name"]=str(budget.budget_name)
    #     budget_item["budget_id"]=str(budget.budget_id)
    #     budget_item["budget_description"]=str(budget.budget_description)
    #     budget_item["budget_frequency"]=str(budget.budget_frequency)
    #     budgetlist.append(budget_item)
    #     print(budget)
    # print(budgets)
    # return jsonify(budgetlist)

if __name__ == "__main__": 
    app.debug = True 
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.config.from_object(__name__)
    celery=create_celery_app(app)
    
    @celery.task()
    def get_products(query): 
        user = crud.get_user_by_email(session["user_email"])
        product_instance=services.ProductFeed()
        db.session.add(product_instance.fetch(query, user.user_id))
        db.session.commit()
        return render_template("home.html")
    app.run(host="0.0.0.0")