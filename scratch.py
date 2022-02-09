
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

      # return f"You want ${path}"

# def homepage():
#     """"Show homepage"""
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
