"""SQLAlchemy Database Setup"""

from flask_sqlalchemy import SQLAlchemy 

db= SQLAlchemy()


class User(db.Model):
    """ User model """
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} password={self.password}'

class Budget(db.Model):
    """ Budgets model """
    __tablename__ = "budgets"
    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_name = db.Column(db.String, nullable=False, unique=True)
    budget_description = db.Column(db.String, nullable=False)
    budget_amount = db.Column(db.Integer, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    user = db.relationship("User", back_populates="users")
    category_id = db.Column(db.Integer, db.ForeignKey(category.category_id))
    category = db.relationship("category", back_populates="categories")
    
    def __repr__(self):
        return f'<Budget category_id={self.category_id} budget_name={self.budget_name} budget_description={self.budget_description}'

class Advice(db.Model):
    """ Advice model """
    __tablename__ = "advice"
    advice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    advice_name = db.Column(db.String(155), nullable=False, unique=True)
    advice_description = db.Column(db.String(500), nullable=False)
    advice_amount = db.Column(db.Integer, nullable=False)
    
    budget_id = db.Column(db.Integer, db.ForeignKey(Budget.budget_id))
    budget = db.relationship("budget", back_populates="budgets")
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    user = db.relationship("User", back_populates="users")
    category_id = db.Column(db.Integer, db.ForeignKey(Categories.category_id))
    category = db.relationship("category", back_populates="categories")
    
    def __repr__(self):
        return f'<Advice category_id={self.category_id} advice_name={self.advice_name} advice_description={self.advice_description}'

class User_Transactions(db.Model):
    """ User transactions model """
    __tablename__ = "user_transactions"
    user_transactions_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User user_transactions_id={self.user_id} email={self.email} password={self.password}'

class Categories(db.Model):
    """ Categories model """
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(155), nullable=False, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    user = db.relationship("User", back_populates="users")
    
    def __repr__(self):
        return f'<Categories category_id={self.category_id} category_name={self.category_name}'

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///myntwise"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app 
    db.init_app(app)

    if __name__ =="__main__":
        from server import app 
        connect_to_db(app)

        db.create_all()
        print("Connected to DB")
