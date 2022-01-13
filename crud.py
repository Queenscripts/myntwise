from model import db, User, User_Transactions, Budget, Categories, Advice, connect_to_db

# CRUD FOR USERS
def get_users():
    """Get all users"""
    return User.query.all()

def create_user(email, password):
    """ Create User, Return User"""
    user = User(email=email, password=password)
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

def create_categories(category_name):
    """Get all categories"""
    category = Categories(
        category_name=category_name
    )
    db.session.add(category)
    db.session.commit()

    return category

# CRUD FOR BUDGETS
def create_budget(budget_name, budget_amount, budget_description, budget_frequency, user_id):
    budget = Budget(
        budget_name=budget_name, 
        budget_amount=budget_amount, 
        budget_description=budget_description, 
        budget_frequency=budget_frequency, 
        user_id=user_id
    )
    db.session.add(budget)
    db.session.commit()

    return budget

def get_budgets():
    """Get all budgets"""
    return Budget.query.all()

# CRUD FOR USER TRANSACTIONS
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

# CRUD FOR ADVICE
def get_advice():
    """Get all advice"""
    return Advice.query.all()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)