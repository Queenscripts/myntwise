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
    query=request.args.get("query")
    if query:
        get_products(query).delay()
    return render_template("index.html")

@app.route("/<path:path>", defaults={'path':''})
def catch_all(path): 
    return render_template("index.html")
 
# # USER ROUTES
@app.route("/signup", methods=["POST"])
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
            return redirect("/login")
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
        return redirect("/")

@app.route("/login", methods=["POST"])
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
    

@app.route("/logout", methods=["GET"])
def logout(): 
    """ Logout User """
    session.clear()
    return redirect("/")

# # BUDGET ROUTE
@app.route("/budget/<id>", methods=["GET"])
def delete_budget(id):
    """Route to delete budget"""
    crud.delete_budget(id)
    db.session.commit()
    return redirect("/budgets")
# #@TODO Route for update

# # USER TRANSACTION ROUTES
@app.route("/api/transactions", methods=["GET", "POST", "PUT", "DELETE"])
def transactions():
    """Show & Handle User Transactions"""
    user = crud.get_user_by_email(session["user_email"])
    transactions = crud.get_user_transactions(user.user_id)
    categories = crud.get_categories()

    if request.method == "GET": 
        parsed_transactions = []
        for transaction in transactions:
            transaction_item={} 
            transaction_item["user_id"]=str(transaction[0].user_id)
            transaction_item["transaction_name"]=str(transaction[0].user_transactions_name)
            transaction_item["transaction_id"]=str(transaction[0].user_transactions_id)
            transaction_item["transaction_amount"]=str(transaction[0].user_transactions_amount)
            transaction_item["transaction_date"]=str(transaction[0].user_transactions_date)
            transaction_item["budget"]=str(transaction[1].budget_name)
            transaction_item["category"]=str(transaction[2].category_name)
            parsed_transactions.append(transaction_item)
        return jsonify(parsed_transactions)

    if request.method == "POST":
        
        request_data = request.get_json(force=True)

        print('DATA', request_data)
        user = crud.get_user_by_email(session["user_email"])
        user_transactions_name = request.form.get("user_transaction_name") or request_data["user_transactions_name"]
        user_transactions_amount = request.form.get("user_transaction_amount") or request_data["user_transactions_amount"]
        user_transactions_date = request.form.get("user_transaction_date") or request_data["user_transactions_date"]
        user_transactions_processed = request_data["user_transactions_processed"]
        # if request_data and request_data["budget"] and request_data["category"]:
        budget = crud.get_budget_by_name(request.form.get("budget")) or crud.get_budget_by_name(request_data["budget"]) or None
        category = crud.get_category(request.form.get("category")) or crud.get_category(request_data["category"]) or None
        if budget == None and category == None:
            new_user_transaction = crud.create_user_transaction(user_transactions_name,user_transactions_amount, user_transactions_date, budget, category, user.user_id, user_transactions_processed)
            db.session.add(new_user_transaction)
            db.session.commit()
        new_user_transaction = crud.create_user_transaction(user_transactions_name,user_transactions_amount, user_transactions_date,budget.budget_id,category.category_id, user.user_id, user_transactions_processed)
        # else: 
            # 
        db.session.add(new_user_transaction)
        db.session.commit()
        flash(f"New user_transaction: {new_user_transaction.user_transactions_name}")
        return redirect("/transactions")

@app.route("/api/transaction/<id>", methods=["GET"])
def delete_transaction(id):
    """Route to delete transaction"""
    crud.delete_transaction(id)
    db.session.commit()
    return redirect("/dashboard#transactions")

# ADVICE ROUTE

# API ROUTES 
@app.route("/api/all-users")
def display_users():
    """Show users"""
    users = crud.get_users()
    usery=[]
    for user in users:
        userz={} 
        
        userz["email"]=str(user.email)
        userz["user_id"]=str(user.user_id)
        usery.append(userz)
    print(usery)
    return jsonify(usery)

@app.route("/api/advice")
def advice():
    """Display advice"""
    ROWS_PER_PAGE = 9
    page = request.args.get('page')
    advice_list = []

    if page:
        advice = crud.get_advice().paginate(page=int(page), per_page=ROWS_PER_PAGE)
        for product in advice.items: 
            advice_item = {}
            advice_item["advice_id"] = str(product.advice_id)
            advice_item["advice_name"] = str(product.advice_name)
            advice_item["advice_description"] = str(product.advice_description)
            advice_item["advice_price"] = str(product.advice_price)
            advice_item["advice_img"] = str(product.advice_img)
            advice_item["advice_info_id"] = str(product.advice_info_id)
            advice_list.append(advice_item)
    else: 
        advice = crud.get_advice().all()
        for product in advice: 
            advice_item = {}
            advice_item["advice_id"] = str(product.advice_id)
            advice_item["advice_name"] = str(product.advice_name)
            advice_item["advice_description"] = str(product.advice_description)
            advice_item["advice_price"] = str(product.advice_price)
            advice_item["advice_img"] = str(product.advice_img)
            advice_item["advice_info_id"] = str(product.advice_info_id)
            advice_list.append(advice_item)
    return jsonify(advice_list)

@app.route("/api/advice/price")
def advice_by_price():
    """Display advice by price - paginated"""
    ROWS_PER_PAGE = 9
    page = request.args.get('page')
    min_price = request.args.get('min')
    max_price = request.args.get('max')
    advice_list = []

    advice = crud.filter_advice_by_price(min_price, max_price).paginate(page=int(page), per_page=ROWS_PER_PAGE)
    for product in advice.items: 
        advice_item = {}
        advice_item["advice_id"] = str(product.advice_id)
        advice_item["advice_name"] = str(product.advice_name)
        advice_item["advice_description"] = str(product.advice_description)
        advice_item["advice_price"] = str(product.advice_price)
        advice_item["advice_img"] = str(product.advice_img)
        advice_item["advice_info_id"] = str(product.advice_info_id)
        advice_list.append(advice_item)
    # else: 
    #     advice = crud.get_advice().all()
    #     for product in advice: 
    #         advice_item = {}
    #         advice_item["advice_id"] = str(product.advice_id)
    #         advice_item["advice_name"] = str(product.advice_name)
    #         advice_item["advice_description"] = str(product.advice_description)
    #         advice_item["advice_price"] = str(product.advice_price)
    #         advice_item["advice_img"] = str(product.advice_img)
    #         advice_item["advice_info_id"] = str(product.advice_info_id)
    #         advice_list.append(advice_item)
    return jsonify(advice_list)

@app.route("/api/user/advice")
def user_advice():
    """Display advice"""
    ROWS_PER_PAGE = 9
    page = request.args.get('page')
    min_price = request.args.get('min')
    max_price = request.args.get('max')

    user = crud.get_user_by_email(session["user_email"])
    if min_price or max_price: 
        users_advice = crud.filter_user_advice_by_price(user.user_id, min_price, max_price).paginate(page=int(page), per_page=ROWS_PER_PAGE)
    else:
        users_advice = crud.get_advice_by_user_id(user.user_id).paginate(page=int(page), per_page=ROWS_PER_PAGE)
    
    advice_list = []
    advice_list.append(users_advice.total)
    for product in users_advice.items: 
        advice_item = {}
        advice_item["advice_id"] = str(product.advice_id)
        advice_item["advice_name"] = str(product.advice_name)
        advice_item["advice_description"] = str(product.advice_description)
        advice_item["advice_price"] = str(product.advice_price)
        advice_item["advice_img"] = str(product.advice_img)
        advice_item["advice_info_id"] = str(product.advice_info_id)
        advice_list.append(advice_item)
    return jsonify(advice_list)

@app.route("/api/budgets", methods=["GET","POST"])
def display_budgets():
    """Show budgets"""
    if request.method == "GET":
        if session and session["user_email"]:
            user = crud.get_user_by_email(session["user_email"])
            # budgets = crud.get_user_budgets(user.user_id)
            user_budgets_categories=crud.get_users_categories(user.user_id)
            print(user_budgets_categories,"CAT")
            budgetlist = []
            for budget in user_budgets_categories:
                print('B', budget)
                budget_item={} 
                budget_item["category"]=str(budget[1].category_name)
                budget_item["category_id"]=int(budget[0].category_id)
                budget_item["user_id"]=int(budget[0].user_id)
                budget_item["budget_name"]=str(budget[0].budget_name)
                budget_item["budget_id"]=str(budget[0].budget_id)
                budget_item["budget_amount"]=str(budget[0].budget_amount)
                budget_item["budget_description"]=str(budget[0].budget_description)
                budget_item["budget_frequency"]=str(budget[0].budget_frequency)
                budgetlist.append(budget_item)
            return jsonify(budgetlist)
    if request.method == "POST":
        request_data = request.get_json(force=True)
        user = crud.get_user_by_email(session["user_email"])
        budget_name = request_data["budget_name"]
        budget_amount = request_data["budget_amount"] 
        budget_description = request_data["budget_description"] 
        budget_frequency = request_data["budget_frequency"] 
        category = crud.get_category(request_data["category"] )

        new_budget = crud.create_budget(budget_name,budget_amount,budget_description,budget_frequency, user.user_id, category.category_id)

        db.session.add(new_budget)
        db.session.commit()
        return redirect("/budgets")

@app.route("/api/categories")
def display_categories(): 
    """Show categories"""
    categories = crud.get_categories()
    categories_list = []
    for category in categories: 
        category_list={}
        category_list["name"]=category.category_name
        category_list["id"]=category.category_id
        categories_list.append(category_list)
    print(categories_list)
    return jsonify(categories_list)

@app.route("/api/reports")
def display_reports(): 
    """Show transactions & budgets reports"""
    user = crud.get_user_by_email(session["user_email"])
    budget_amount = crud.get_budget_amount(user.user_id)
    budget_count = crud.get_budgets_count(user.user_id)
    transactions_count = crud.get_transactions_count(user.user_id)
    transactions_sum = crud.get_total_sum_transactions(user.user_id)
    get_total_budget_diff = crud.get_total_budget_diff(user.user_id)
    cat_count = crud.get_categories_count(user.user_id)
    total_saved = crud.get_total_transaction_saved(user.user_id)
    total_transactions = crud.get_total_sum_transactions(user.user_id)
    get_total_saved_transactions_count = crud.get_total_saved_transactions_count(user.user_id)
    user_report = {}
    user_report["total_budget_amount"] = int(budget_amount[0][0])
    user_report["budget_count"] = int(budget_count)
    user_report["transactions_count"] = int(transactions_count)
    budget_differences=[]
    for budget in get_total_budget_diff: 
        budget_diff={}
        budget_diff["budget"] = budget[1]
        budget_diff["diff"] = budget[0]
        budget_diff["total_transactions_amount"] = budget[2]
        budget_diff["total_transactions"] = budget[3]
        budget_differences.append(budget_diff)
    user_report["budget_differences"] = budget_differences
    user_report["transactions_sum"] = int(transactions_sum[0][0])
    user_report["cat_count"] = int(cat_count)
    # if total_saved:
    #     user_report["total_saved"] = int(total_saved[0])
    user_report["total_transactions"] = int(total_transactions[0][0])
    user_report["total_saved_count"] = int(get_total_saved_transactions_count)
    print(get_total_budget_diff)
    return jsonify(user_report)

if __name__ == "__main__": 
    app.debug = True 
    app.DEBUG_TB_INTERCEPT_REDIRECTS = False
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