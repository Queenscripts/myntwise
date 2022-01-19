from model import db, User, User_Transactions, Budget, Categories, Advice, connect_to_db
# from server import budgets, transactions

# CRUD FOR USERS
def get_users():
    """Get all users"""
    return User.query.all()

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

def get_category(category_name):
    """ Get Category Info"""
    return Categories.query.filter_by(category_name=category_name).first()

def create_categories(category_name):
    """Get all categories"""
    category = Categories(
        category_name=category_name
    )
    db.session.add(category)
    db.session.commit()

    return category

# CRUD FOR BUDGETS
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

def get_budgets():
    """Get all budgets"""
    return Budget.query.all()

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
# CRUD FOR USER TRANSACTIONS
def get_user_transactions(user_id): 
    """ Get all transactions for user """
    return User_Transactions.query.filter_by(user_id=user_id).all()


def create_user_transaction(user_transactions_name, user_transactions_amount, user_transactions_date, budget_id, category_id, user_id): 
    """ Create User Transaction """
    transaction = User_Transactions(
        user_transactions_name=user_transactions_name, 
        user_transactions_amount=user_transactions_amount, 
        user_transactions_date=user_transactions_date, 
        budget_id=budget_id, 
        category_id=category_id,
        user_id=user_id
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction
    
# CRUD FOR ADVICE
def get_advice():
    """Get all advice"""
    return Advice.query.all()

def get_advice_by_id(advice_id): 
    """Get advice by ID"""
    return Advice.get(advice_id)

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

# REPORTS 
def get_transactions_count(user_id): 
    """ Get number of transactions for user """
    return User_Transactions.query.filter_by(user_id=user_id).count()

def get_budgets_count(user_id): 
    """ Get number of budgets for user """
    return Budget.query.filter_by(user_id=user_id).count()

def get_categories_count(user_id): 
    """ Get number of budgets by category for user """
    return Budget.query.filter_by(user_id=user_id).join(Categories, Budget.category_id==Categories.category_id).count()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)