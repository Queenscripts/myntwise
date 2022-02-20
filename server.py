# from unicodedata import category
from flask import Flask, render_template, jsonify, flash, session, redirect, request, url_for
from model import connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
import crud
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from celerydb import create_celery_app
import services
from authlib.integrations.flask_client import OAuth
import os
from config import Config
from sqlalchemy import create_engine

app = Flask(__name__, static_folder="./static")
app.config.from_object(Config)

oauth = OAuth(app)

SESSION_TYPE = "filesystem"

app.secret_key = "ABCSECRETDEF"

@app.route('/google/')
def google():

    GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
    GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    
    if(user and user.get('at_hash')):
        user_in_db = crud.get_user_by_email(user.email)

        if user_in_db:
            session["user_email"]=user_in_db.email
            return redirect("/")
        else:
            hashed_pass = generate_password_hash(user.get('at_hash'))
            # Save user image
            new_user = crud.create_user(user.name,user.email, hashed_pass)

            db.session.add(new_user)
            db.session.commit()

            session["user_email"]= new_user.email
            return redirect('/')

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
        user = crud.get_user_by_email(session["user_email"])
        user_transactions_name = request.form.get("user_transaction_name") or request_data["user_transactions_name"]
        user_transactions_amount = request.form.get("user_transaction_amount") or request_data["user_transactions_amount"]
        user_transactions_date = request.form.get("user_transaction_date") or request_data["user_transactions_date"]
        user_transactions_processed = request_data["user_transactions_processed"]
        img = request_data["img"] or None
        # if request_data and request_data["budget"] and request_data["category"]:
        budget = crud.get_budget_by_name(request.form.get("budget")) or crud.get_budget_by_name(request_data["budget"]) or None
        category = crud.get_category(request.form.get("category")) or crud.get_category(request_data["category"]) or None
        if budget == None or category == None:
            new_user_transaction = crud.create_user_transaction(user_transactions_name,user_transactions_amount, user_transactions_date, budget, category, user.user_id, user_transactions_processed,img)
            db.session.add(new_user_transaction)
            db.session.commit()
        else:
            new_user_transaction = crud.create_user_transaction(user_transactions_name,user_transactions_amount, user_transactions_date,budget.budget_id,category.category_id, user.user_id, user_transactions_processed, img)

            db.session.add(new_user_transaction)
            db.session.commit()
            new_budget = crud.get_budget_by_id(new_user_transaction.budget_id)
            new_category = crud.get_category_by_id(new_user_transaction.category_id)
        # flash(f"New user_transaction: {new_user_transaction.user_transactions_name}")
        return jsonify({
            "transaction_id" : new_user_transaction.user_transactions_id,
            "transaction_name":new_user_transaction.user_transactions_name,
            "transaction_amount":new_user_transaction.user_transactions_amount,
            "transaction_date": new_user_transaction.user_transactions_date,
            "budget": new_budget.budget_name,
            "category": new_category.category_name

        })

    if request.method == "PUT":
        user = crud.get_user_by_email(session["user_email"])
        request_data = request.get_json(force=True)
        budget = crud.get_budget_by_name(request.json.get('budget'))
        category = crud.get_category(request.json.get('category'))
        user_transactions_id = request_data['transaction_id']
        transaction = crud.get_user_transaction(user.user_id, user_transactions_id)
        transaction.user_transactions_name = request.json.get('user_transactions_name',transaction.user_transactions_name)
        transaction.user_transactions_amount = request.json.get('user_transactions_amount',transaction.user_transactions_amount)
        transaction.budget_id = budget.budget_id
        transaction.category_id = category.category_id
        transaction.user_transactions_date = request.json.get('user_transactions_date',transaction.user_transactions_date)
        db.session.commit()
        b = crud.get_budget_by_id(transaction.budget_id)
        c = crud.get_category_by_id(transaction.category_id)
        return jsonify(
            {
                "transaction_id": str(transaction.user_transactions_id),
                "transaction_name": str(transaction.user_transactions_name),
                "transaction_amount": str(transaction.user_transactions_amount),
                "transaction_date": str(transaction.user_transactions_date),
                "budget": b.budget_name, 
                "category": c.category_name,
                "user_id": str(user.user_id)
            }
        )

@app.route("/api/saved")
def saved_transactions(): 
    """Retrieve saved transactions"""
    user = crud.get_user_by_email(session["user_email"])
    saved = crud.get_saved_transactions(user.user_id)
    saved_list = []
    for i in saved: 
        item={}
        item["img"] = i.img 
        item["price"] = i.user_transactions_amount
        item["name"] = i.user_transactions_name
        saved_list.append(item)
    return jsonify(saved_list)

@app.route("/api/transaction/<id>", methods=["GET"])
def delete_transaction(id):
    """Route to delete transaction"""
    crud.delete_transaction(id)
    db.session.commit()
    return redirect("/dashboard#transactions")


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
    return jsonify(usery)

@app.route("/api/advice")
def advice():
    """Display advice"""
    ROWS_PER_PAGE = 9
    page = request.args.get('page')
    advice_list = []

    if page:
        advice = crud.get_advice().paginate(page=int(page), per_page=ROWS_PER_PAGE)
        advice_list.append(advice.total)

        # advice_list.append(len(advice.items))

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
        advice_list.append(len(advice))
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
    if page:
        advice = crud.filter_advice_by_price(min_price, max_price).paginate(page=int(page), per_page=ROWS_PER_PAGE)
        advice_list.append(advice.total)
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
        advice = crud.filter_all_advice_by_price(min_price, max_price)
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
            budgetlist = []
            for budget in user_budgets_categories:
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
        new_category = crud.get_category_by_id(new_budget.category_id)
        db.session.add(new_budget)
        db.session.commit()
        return jsonify({
            "budget_id": new_budget.budget_id,
            "budget_name":new_budget.budget_name,
            "budget_description": new_budget.budget_description,
            "budget_amount": new_budget.budget_name,
            "budget_frequency": new_budget.budget_frequency,
            "user_id": new_budget.user_id,
            "category": new_category.category_name
            })

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
    return jsonify(categories_list)

@app.route("/api/reports")
def display_reports(): 
    """Show transactions & budgets reports"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    user = crud.get_user_by_email(session["user_email"])
    budgets = crud.get_budgets_and_transactions(user.user_id)
    budget_amount = crud.get_budget_amount(user.user_id)
    budget_count = crud.get_budgets_count(user.user_id)
    transactions_count = crud.get_transactions_count(user.user_id)
    transactions_sum = crud.get_total_sum_transactions(user.user_id)
    get_total_budget_diff = crud.get_total_budget_diff(user.user_id)
    cat_count = crud.get_categories_count(user.user_id)
    
    total_transactions = crud.get_total_sum_transactions(user.user_id)
    get_total_saved_transactions_count = crud.get_total_saved_transactions_count(user.user_id)
    user_report = {}
    transactions_by_date=[]
    transactions_by_price=[]
    budgets_info = []
    for info in budgets:
        budget_info = {} 
        budget_info["name"]=info[0].budget_name
        budget_info["amount"]=info[0].budget_amount
        budgets_info.append(budget_info)
    user_report['budget_info'] = budgets_info 
    if start_date or end_date:
        frequency = crud.filter_user_transactions_by_date(user.user_id,start_date,end_date)
        for transaction in frequency: 
            transaction_frequency = {}
            category = crud.get_category_by_id(transaction.category_id)
            budget = crud.get_budget_by_id(transaction.budget_id)
            transaction_frequency["user_transactions_id"],transaction_frequency["user_transactions_name"],transaction_frequency["transaction_amount"],transaction_frequency["transaction_date"],transaction_frequency["transaction_budget"],transaction_frequency["transaction_category"]=transaction.user_transactions_id, transaction.user_transactions_name, transaction.user_transactions_amount, transaction.user_transactions_date, budget.budget_name, category.category_name
            transactions_by_date.append(transaction_frequency)
    user_report["dated_transactions"] = transactions_by_date
    if min_price or max_price:
        price = crud.filter_user_transactions_by_price(user.user_id, min_price, max_price)
        
        for transaction in price: 
            transaction_price_range = {}
            category = crud.get_category_by_id(transaction.category_id)
            budget = crud.get_budget_by_id(transaction.budget_id)
            transaction_price_range["user_transactions_id"],transaction_price_range["user_transactions_name"],transaction_price_range["transaction_amount"],transaction_price_range["transaction_date"],transaction_price_range["transaction_budget"],transaction_price_range["transaction_category"]=transaction.user_transactions_id, transaction.user_transactions_name, transaction.user_transactions_amount, transaction.user_transactions_date, budget.budget_name, category.category_name
            transactions_by_price.append(transaction_price_range)
    user_report["price_ranged_transactions"] = transactions_by_price

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
    user_report["total_transactions"] = int(total_transactions[0][0])
    user_report["total_saved_count"] = int(get_total_saved_transactions_count)
    return jsonify(user_report)

if __name__ == "__main__": 
    app.debug = False 
    app.DEBUG_TB_INTERCEPT_REDIRECTS = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db(app)
    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(DB_URI)

    db.init_app(app)

    connect_to_db(app)
    DebugToolbarExtension(app)

    celery=create_celery_app(app)
    # app.run()
    @celery.task()
    def get_products(query): 
        product_instance=services.ProductFeed()
        if session and session.get("user_email"):
            user = crud.get_user_by_email(session["user_email"])
            db.session.add(product_instance.fetch(query, user.user_id))
            db.session.commit()
        db.session.add(product_instance.generate(query))
        db.session.commit()
        
    app.run(host='127.0.0.1',debug=False)