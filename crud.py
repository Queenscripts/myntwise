import model
from model import db, User, User_Transactions, Budget, Categories, Advice, connect_to_db
# from server import budgets, transactions
from sqlalchemy.sql import functions
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine,  Table, MetaData, Column, Integer, String
from sqlalchemy.orm import Session
import os 

engine = create_engine(os.environ["POSTGRES_URI"])
metadata = MetaData(engine)


session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

# CRUD FOR USERS
def get_users():
    """Get all users"""
    return session.query(User).all()

def create_user(name, email, password):
    """ Create User, Return User"""
    user = Table("users", metadata, autoload=True)
    engine.execute(user.insert(),name=name, email=email, password=password)
    # user = User(name=name, email=email, password=password)
    # db.session.add(user)
    # db.session.commit()

    return user

def get_user(id): 
    """ Get user by id """
    return session.query(User).get(id)

def get_user_by_email(email): 
    """ Get user by email """
    return session.query(User).filter_by(email=email).first()

# CRUD FOR CATEGORIES
def get_categories():
    """Get all categories"""
    return session.query(Categories).all()

def get_users_categories(user_id):
    """Get categories ids"""
    return session.query(Budget,Categories).filter(Budget.user_id==user_id).filter(Budget.category_id==Categories.category_id).all()

def get_category(category_name):
    """ Get Category Info"""
    return session.query(Categories).filter_by(category_name=category_name).first()

def get_category_by_id(category_id):
    """ Get Category by ID"""
    return session.query(Categories).get(category_id)

def create_categories(category_name):
    """Get all categories"""
    category = Table("categories", metadata, autoload=True)
    engine.execute(category.insert(), category_name=category_name)
    new_category = Session(engine).query(Categories).filter_by(category_name=category_name).first()
    # db.session.add(category)
    # db.session.commit()
    return new_category

# CRUD FOR BUDGETS
def get_budget_by_id(id):
    """ Return budget by ID"""
    return session.query(Budget).get(id)

def create_budget(budget_name, budget_amount, budget_description, budget_frequency, user_id, category_id):
    budget = Table("budgets", metadata, autoload=True)
    engine.execute(budget.insert(), 
        budget_name=budget_name, 
        budget_amount=budget_amount, 
        budget_description=budget_description, 
        budget_frequency=budget_frequency, 
        user_id=user_id,
        category_id=category_id)
    new_budget = Session(engine).query(Budget).filter_by(budget_name=budget_name).first()
    #  Budget(
    #     budget_name=budget_name, 
    #     budget_amount=budget_amount, 
    #     budget_description=budget_description, 
    #     budget_frequency=budget_frequency, 
    #     user_id=user_id,
    #     category_id=category_id
    # )
    # db.session.add(budget)
    # db.session.commit()

    return new_budget

def get_budgets_and_transactions(user_id):
    """Get all budgets"""
    return session.query(Budget, User_Transactions).filter_by(user_id=user_id).join(User_Transactions, Budget.budget_id==User_Transactions.budget_id, isouter=True).all()

def get_user_budgets(user_id):
    """" Get all budgets for user """
    return session.query(Budget).filter_by(user_id=user_id).all()

def get_budget_by_name(budget_name):
    """Get budget info by name"""
    return session.query(Budget).filter_by(budget_name=budget_name).first()

def delete_budget(id):
    """Delete Budget"""
    obj= session.query(Budget).filter(Budget.budget_id==id).first()
    session.delete(obj)
    session.commit()
    return f"Deleted budget id: {id}"

def update_budget(id,entity):
    """Update budget"""
    budget = Budget.query.get(id)
    budget.entity.name = entity.vall
    db.session.commit()

# CRUD FOR USER TRANSACTIONS
def get_user_transactions(user_id): 
    """ Get all transactions for user """
    return session.query(User_Transactions, Budget, Categories).filter_by(user_id=user_id).filter(User_Transactions.budget_id==Budget.budget_id).filter(User_Transactions.category_id==Categories.category_id).all()

def get_user_transaction(user_id, user_transactions_id):
    """Get single transaction"""
    return session.query(User_Transactions).filter_by(user_id=user_id).filter_by(user_transactions_id=user_transactions_id).first()

def create_user_transaction(user_transactions_name, user_transactions_amount, user_transactions_date, budget_id, category_id, user_id, user_transactions_processed, img): 
    """ Create User Transaction """
    new_transaction = Table("user_transactions", metadata, autoload=True)
    engine.execute(new_transaction.insert(), user_transactions_name=user_transactions_name, user_transactions_amount=user_transactions_amount, user_transactions_date=user_transactions_date, budget_id=budget_id, category_id=category_id, user_id=user_id,user_transactions_processed=user_transactions_processed,img=img)
    transaction = Session(engine).query(User_Transactions).filter_by(user_transactions_name=user_transactions_name).first()
    # transaction = User_Transactions(
    #     user_transactions_name=user_transactions_name, 
    #     user_transactions_amount=user_transactions_amount, 
    #     user_transactions_date=user_transactions_date, 
    #     budget_id=budget_id, 
    #     category_id=category_id,
    #     user_id=user_id,
    #     user_transactions_processed=user_transactions_processed,
    #     img=img
    # )
    # db.session.add(transaction)
    # db.session.commit()
    return transaction
    
def update_user_transaction(id,entity):
    """Update Transaction"""
    transaction = session.query(User_Transactions).get(id)
    transaction.entity.name = entity.vall
    db.session.commit()

def delete_transaction(id):
    """Delete Transaction"""
    return session.query(User_Transactions).filter_by(user_transactions_id=id).delete()
    # return f"Deleted transaction id: {id}"

def filter_by_date(user_id, start_date, end_date): 
    """Get all transactions by date range"""
    return session.query(User_Transactions).filter(User_Transactions.user_transactions_date>=start_date).filter(User_Transactions.user_transactions_date<=end_date)
# CRUD FOR ADVICE
def get_advice():
    """Get all advice"""
    return session.query(Advice)

def get_advice_by_name(advice_name):
    """Get all advice"""
    return session.query(Advice).filter_by(advice_name=advice_name).first()

def get_advice_by_user_id(user_id):
    """Get all advice""" 
    # Advice.query.filter_by(user_id=user_id)
    return session.query(Advice).filter_by(user_id=user_id)

def get_advice_by_id(advice_id): 
    """Get advice by ID"""
    #  Advice.get(advice_id)
    return session.query(Advice).get(advice_id)

def filter_advice_by_price(min_price, max_price):
    """Filter advice by price"""
    # Advice.query.filter(Advice.advice_price>min_price).filter(Advice.advice_price<max_price)
    return session.query(Advice).filter(Advice.advice_price>min_price).filter(Advice.advice_price<max_price)

def filter_all_advice_by_price(min_price, max_price):
    """Filter advice by price"""
    return session.query(Advice).filter(Advice.advice_price>min_price).filter(Advice.advice_price<max_price).all()

def filter_user_advice_by_price(user_id,min_price, max_price):
    """Filter advice by price"""
    return session.query(Advice).filter_by(user_id=user_id).filter(Advice.advice_price>min_price).filter(Advice.advice_price<max_price)

def filter_advice_by_category(category_id):
    """Filter advice by price"""
    return session.query(Advice).filter(Advice.category_id==category_id).all()

def create_advice(advice_name,  advice_price, advice_description, advice_info_id, category_id, advice_img):
    """Create advice"""
    # advice = Advice(
    #     advice_name=advice_name, 
    #     advice_price=advice_price, 
    #     advice_description= advice_description, 
    #     advice_info_id=advice_info_id,
    #     category_id=category_id,
    #     advice_img=advice_img
    # )
    new_advice = Table("advice", metadata, autoload=True)
    engine.execute(new_advice.insert(),advice_name=advice_name, 
        advice_price=advice_price, 
        advice_description= advice_description, 
        advice_info_id=advice_info_id,
        category_id=category_id,
        advice_img=advice_img)
    advice = Session(engine).query(Advice).filter_by(advice_name=advice_name).first()
    # db.session.add(advice)
    # db.session.commit()

    return advice

def create_advice_for_user(advice_name,  advice_price, advice_description, advice_info_id, category_id, advice_img,user_id):
    """Create advice"""
    new_advice = Table("advice", metadata, autoload=True)
    engine.execute(
        new_advice.insert(),advice_name=advice_name, 
        advice_price=advice_price, 
        advice_description= advice_description, 
        advice_info_id=advice_info_id,
        category_id=category_id,
        advice_img=advice_img,
        user_id=user_id
        )
    advice = Session(engine).query(Advice).filter_by(advice_name=advice_name).first()

    return advice

# REPORTS 
def get_transactions_count(user_id): 
    """ Get number of transactions for user """
    #  User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_processed==True).count()
    return session.query(User_Transactions).filter_by(user_id=user_id).filter(User_Transactions.user_transactions_processed==True).count()
def get_budgets_count(user_id): 
    """ Get number of budgets for user """
    # return Budget.query.filter_by(user_id=user_id).count()
    return session.query(Budget).filter_by(user_id=user_id).count()

def filter_user_transactions_by_price(user_id,min_price, max_price):
    """Filter advice by price"""
    # return User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_amount>=min_price).filter(User_Transactions.user_transactions_amount<=max_price).filter(User_Transactions.user_transactions_processed==True).all()
    return session.query(User_Transactions).query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_amount>=min_price).filter(User_Transactions.user_transactions_amount<=max_price).filter(User_Transactions.user_transactions_processed==True).all()

def filter_user_transactions_by_date(user_id,start_date, end_date):
    """Filter advice by price"""
    # return User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_date>=start_date).filter(User_Transactions.user_transactions_date<=end_date).filter(User_Transactions.user_transactions_processed==True).all()
    return session.query(User_Transactions).filter_by(user_id=user_id).filter(User_Transactions.user_transactions_date>=start_date).filter(User_Transactions.user_transactions_date<=end_date).filter(User_Transactions.user_transactions_processed==True).all()

def get_saved_transactions(user_id):
    """Get user's saved advice"""
    # return User_Transactions.query.filter_by(user_id=user_id).filter(User_Transactions.user_transactions_processed==False).all()
    return session.query(User_Transactions).filter_by(user_id=user_id).filter(User_Transactions.user_transactions_processed==False).all()

def get_categories_count(user_id): 
    """ Get number of budgets by category for user """
    # return Budget.query.filter_by(user_id=user_id).join(Categories, Budget.category_id==Categories.category_id).count()
    return session.query(Budget).filter_by(user_id=user_id).join(Categories, Budget.category_id==Categories.category_id).count()

def get_total_budget_diff(user_id): 
    """Get difference of budgets from transactions"""
    # return db.session.query(Budget.budget_amount-functions.sum(User_Transactions.user_transactions_amount), Budget.budget_name, functions.sum(User_Transactions.user_transactions_amount), functions.count(User_Transactions.user_transactions_processed==True)).filter(Budget.user_id==user_id).filter(User_Transactions.budget_id==Budget.budget_id).filter(User_Transactions.user_transactions_processed==True).group_by(Budget.budget_id).all()
    return session.query(Budget.budget_amount-functions.sum(User_Transactions.user_transactions_amount), Budget.budget_name, functions.sum(User_Transactions.user_transactions_amount), functions.count(User_Transactions.user_transactions_processed==True)).filter(Budget.user_id==user_id).filter(User_Transactions.budget_id==Budget.budget_id).filter(User_Transactions.user_transactions_processed==True).group_by(Budget.budget_id).all()

def get_budget_amount(user_id): 
    """Get total of prices of transactions- purchased"""
    # return db.session.query(functions.sum(Budget.budget_amount)).filter(Budget.user_id==user_id).all()
    return session.query(functions.sum(Budget.budget_amount)).filter(Budget.user_id==user_id).all()
    
def get_total_transaction_saved(user_id): 
    """Get all transactions- not purchased"""
    # return db.session.query(functions.sum(User_Transactions.user_transactions_amount)).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).all()
    return session.query(functions.sum(User_Transactions.user_transactions_amount)).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).all()

def get_total_transactions(user_id): 
    """Get all transactions info- not purchased"""
    # return User_Transactions.query.filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).all()
    return session.query(User_Transactions).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).all()
    
def get_total_saved_transactions_count(user_id): 
    """Get saved transactions count"""
    # User_Transactions.query.filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).count()
    return session.query(User_Transactions).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==False).count()

def get_total_sum_transactions(user_id): 
    """Get all transactions info- not purchased"""
    # db.session.query(functions.sum(User_Transactions.user_transactions_amount)).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==True).all()
    return session.query(functions.sum(User_Transactions.user_transactions_amount)).filter(User_Transactions.user_id==user_id).filter(User_Transactions.user_transactions_processed==True).all()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)