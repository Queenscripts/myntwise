import os 
import crud 
import model 
import server 
import json 

os.system('dropdb myntwise --if-exists')
os.system('createdb myntwise')

model.connect_to_db(server.app)
model.db.create_all()

# SEED USERS TABLE 

# for n in range(10):
#     name = f"User|{n}"
#     email = f'user{n}@test.com'
#     password = 'test'
#     user = crud.create_user(name, email, password)

# SEED CATEGORIES TABLE 

with open('data/categories.json') as c:
    categories_data = json.loads(c.read())

categories_db = []

for category in categories_data: 
    category_name  = (
        category['category_name'],
    )
    db_category = crud.create_categories(category_name)
    categories_db.append(db_category)


# SEED BUDGETS TABLE 

# with open('data/budgets.json') as b:
#     budgets_data = json.loads(b.read())

# budgets_in_db = []

# for budget in budgets_data: 
#     budget_name, budget_amount, budget_description, budget_frequency, user_id, category_id  = (
#         budget['budget_name'],
#         budget['budget_amount'],
#         budget['budget_description'],
#         budget['budget_frequency'],
#         budget['user_id'],
#         budget['category_id']
#     )
#     db_budget = crud.create_budget(budget_name, budget_amount, budget_description, budget_frequency, user_id, category_id)
#     budgets_in_db.append(db_budget)

# SEED TRANSACTIONS TABLE 

# with open('data/user_transactions.json') as t:
#     user_transactions = json.loads(t.read())

# transactions_in_db = []

# for transaction in user_transactions: 
#     user_transactions_name, user_transactions_amount, user_transactions_date, budget_id, category_id, user_id, user_transactions_processed  = (
#         transaction['user_transactions_name'],
#         transaction['user_transactions_amount'],
#         transaction['user_transactions_date'],
#         transaction['budget_id'],
#         transaction['category_id'],
#         transaction['user_id'],
#         transaction['user_transactions_processed']
#     )
#     db_user_transaction = crud.create_user_transaction(user_transactions_name, user_transactions_amount, user_transactions_date, budget_id, category_id, user_id,user_transactions_processed, "")
#     transactions_in_db.append(db_user_transaction)


# SEED ADVICE TABLE 

with open('data/advice.json') as a:
    advice_items = json.loads(a.read())

advice_in_db = []

for advice in advice_items: 
    advice_name, advice_price, advice_description, advice_info_id, category_id, advice_img  = (
        advice['advice_name'],
        advice['advice_price'],
        advice['advice_description'],
        advice['advice_info_id'],
        advice['category_id'],
        advice['advice_img'],
        
    )
    db_advice = crud.create_advice(advice_name, advice_price, advice_description, advice_info_id, category_id, advice_img)
    advice_in_db.append(db_advice)


