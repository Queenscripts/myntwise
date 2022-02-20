import model
from model import db, User, User_Transactions, Budget, Categories, Advice, connect_to_db
# from server import budgets, transactions
from sqlalchemy.sql import functions
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os 

engine = create_engine(os.environ["POSTGRES_URI"])

session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

# CRUD FOR USERS
def get_users():
    """Get all users"""
    return session.query(User).all()

def create_user(name, email, password):
    """ Create User, Return User"""
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return user

def get_user(id): 
    """ Get user by id """
    return User.get(id)

def get_user_by_email(email): 
    """ Get user by email """
    return User.query.filter_by(email=email).first()

# CRUD FOR CATEGORIES
def get_categories():
    """Get all categories"""
    return Categories.query.all()

def get_users_categories(user_id):
    """Get categories ids"""
    return db.session.query(Budget,Categories).filter(Budget.user_id==user_id).filter(Budget.category_id==Categories.category_id).all()

def get_category(category_name):
    """ Get Category Info"""
    return Categories.query.filter_by(category_name=category_name).first()

def get_category_by_id(category_id):
    """ Get Category by ID"""
    return db.session.query(Categories).get(category_id)

def create_categories(category_name):
    """Get all categories"""
    category = Categories(
        category_name=category_name
    )
    db.session.add(category)
    db.session.commit()

    return category

# CRUD FOR BUDGETS
def get_budget_by_id(id):
    """ Return budget by ID"""
    return db.session.query(Budget).get(id)

def create_budget(budget_name, budget_amount, budget_description, budget_frequency, user_id, category_id):
    budget = Budget(
        budget_name=budget_name, 
        budget_amount=budget_amount, 
        budget_description=budget_description, 
        budget_frequency=budget_frequency, 
        user_id=user_id,
        category_id=category_id
    )
    db.session.add(budget)
    db.session.commit()

    return budget

def get_budgets_and_transactions(user_id):
    """Get all budgets"""
    return db.session.query(Budget, User_Transactions).filter_by(user_id=user_id).join(User_Transactions, Budget.budget_id==User_Transactions.budget_id, isouter=True).all()

def get_user_budgets(user_id):
    """" Get all budgets for user """
    return Budget.query.filter_by(user_id=user_id).all()

def get_budget_by_name(budget_name):
    """Get budget info by name"""
    return Budget.query.filter_by(budget_name=budget_name).first()

def delete_budget(id):
    """Delete Budget"""
    Budget.query.filter_by(budget_id=id).delete()
    db.session.commit()
    return f"Deleted budget id: {id}"

def update_budget(id,entity):
    """Update budget"""
    budget = Budget.query.get(id)
    budget.entity.name = entity.vall
    db.session.commit()

# CRUD FOR USER TRANSACTIONS
def get_user_transactions(user_id): 
    """ Get all transactions for user """
    return db.session.query(User_Transactions, Budget, Categories).filter_by(user_id=user_id).filter(User_Transactions.budget_id==Budget.budget_id).filter(User_Transactions.category_id==Categories.category_id).all()

def get_user_transaction(user_id, user_transactions_id):
    """Get single transaction"""
    return db.session.query(User_Transactions).filter_by(user_id=user_id).filter_by(user_transactions_id=user_transactions_id).first()

def create_user_transaction(user_transactions_name, user_transactions_amount, user_transactions_date, budget_id, category_id, user_id, user_transactions_processed, img): 
    """ Create User Transaction """
    transaction = User_Transactions(
        user_transactions_name=user_transactions_name, 
        user_transactions_amount=user_transactions_amount, 
        user_transactions_date=user_transactions_date, 
        budget_id=budget_id, 
        category_id=category_id,
        user_id=user_id,
        user_transactions_processed=user_transactions_processed,
        img=img
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction
    
def update_user_transaction(id,entity):
    """Update Transaction"""
    transaction = User_Transactions.query.get(id)
    transaction.entity.name = entity.vall
    db.session.commit()

def delete_transaction(id):
    """Delete Transaction"""
    User_Transactions.query.filter_by(user_transactions_id=id).delete()
    db.session.commit()
    return f"Deleted transaction id: {id}"

def filter_by_date(user_id, start_date, end_date): 
    """Get all transactions by date range"""
    return User_Transactions.query.filter(User_Transactions.user_transactions_date>=start_date).filter(User_Transactions.user_transactions_date<=end_date)
# CRUD FOR ADVICE
def get_advice():
    """Get all advice"""
    return Advice.query

def get_advice_by_name(advice_name):
    """Get all advice"""
    return Advice.query.filter_by(advice_name=advice_name).first()

def get_advice_by_user_id(user_id):
    """Get all advice"""
    return Advice.query.filter_by(user_id=user_id)

def get_advice_by_id(advice_id): 
    """Get advice by ID"""
    return Advice.get(advice_id)

def filter_advice_by_price(min_price, max_price):
    """Filter advice by price"""
    return Advice.query.filter(Advice.advice_price>min_price).filter(Advice.advice_price<max_price)

def filter_all_advice_by_price(min_price, max_price):
    """Filter advice by price"""
    return Advice.query.filter(Advice.advice_price>min_price).filter(Advice.advice_price<max_price).all()

def filter_user_advice_by_price(user_id,min_price, max_price):
    """Filter advice by price"""
    return Advice.query.filter_by(user_id=user_id).filter(Advice.advice_price>min_price).filter(Advice.advice_price<max_price)

def filter_advice_by_category(category_id):
    """Filter advice by price"""
    return Advice.query.filter(Advice.category_id==category_id).all()

def create_advice(advice_name,  advice_price, advice_description, advice_info_id, category_id, advice_img):
    """Create advice"""
    advice = Advice(
        advice_name=advice_name, 
        advice_price=advice_price, 
        advice_description= advice_description, 
        advice_info_id=advice_info_id,
        category_id=category_id,
        advice_img=advice_img
    )
    db.session.add(advice)
    db.session.commit()

    return advice

def create_advice_for_user(advice_name,  advice_price, advice_description, advice_info_id, category_id, advice_img,user_id):
    """Create advice"""
    advice = Advice(
        advice_name=advice_name, 
        advice_price=advice_price, 
        advice_description= advice_description, 
        advice_info_id=advice_info_id,
        category_id=category_id,
        advice_img=advice_img,
        user_id=user_id
    )
    db.session.add(advice)
    db.session.commit()

    return advice

# REPORTS 
def get_transactions_count(user_id): 
    """ Get number of transactions for user """
    return User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_processed==True).count()

def get_budgets_count(user_id): 
    """ Get number of budgets for user """
    return Budget.query.filter_by(user_id=user_id).count()

def filter_user_transactions_by_price(user_id,min_price, max_price):
    """Filter advice by price"""
    return User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_amount>=min_price).filter(User_Transactions.user_transactions_amount<=max_price).filter(User_Transactions.user_transactions_processed==True).all()

def filter_user_transactions_by_date(user_id,start_date, end_date):
    """Filter advice by price"""
    return User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_date>=start_date).filter(User_Transactions.user_transactions_date<=end_date).filter(User_Transactions.user_transactions_processed==True).all()

def get_saved_transactions(user_id):
    """Get user's saved advice"""
    return User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_processed==False).all()
def get_categories_count(user_id): 
    """ Get number of budgets by category for user """
    return Budget.query.filter_by(user_id=user_id).join(Categories, Budget.category_id==Categories.category_id).count()

def get_total_budget_diff(user_id): 
    """Get difference of budgets from transactions"""
    return db.session.query(Budget.budget_amount-functions.sum(User_Transactions.user_transactions_amount), Budget.budget_name, functions.sum(User_Transactions.user_transactions_amount), functions.count(User_Transactions.user_transactions_processed==True)).filter(Budget.user_id==user_id).filter(User_Transactions.budget_id==Budget.budget_id).filter(User_Transactions.user_transactions_processed==True).group_by(Budget.budget_id).all()

def get_budget_amount(user_id): 
    """Get total of prices of transactions- purchased"""
    return db.session.query(functions.sum(Budget.budget_amount)).filter(Budget.user_id==user_id).all()

def get_total_transaction_saved(user_id): 
    """Get all transactions- not purchased"""
    return db.session.query(functions.sum(User_Transactions.user_transactions_amount)).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).all()

def get_total_transactions(user_id): 
    """Get all transactions info- not purchased"""
    return User_Transactions.query.filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).all()

def get_total_saved_transactions_count(user_id): 
    """Get saved transactions count"""
    return User_Transactions.query.filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).count()


def get_total_sum_transactions(user_id): 
    """Get all transactions info- not purchased"""
    return db.session.query(functions.sum(User_Transactions.user_transactions_amount)).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==True).all()



if __name__ == "__main__":
    from server import app
    connect_to_db(app)