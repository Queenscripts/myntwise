"""SQLAlchemy Database Setup"""

from xmlrpc.client import Boolean
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import func

db= SQLAlchemy()


class User(db.Model):
    """ User model """
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.name} email={self.email} password={self.password}>'

class Categories(db.Model):
    """ Categories model """
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(155), nullable=False, unique=True)
    
    # user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    # user = db.relationship("User", backref="users")
    
    def __repr__(self):
        return f'<Categories category_id={self.category_id} category_name={self.category_name}'
class Budget(db.Model):
    """ Budgets model """
    __tablename__ = "budgets"
    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    budget_name = db.Column(db.String, nullable=False, unique=True)
    budget_description = db.Column(db.String, nullable=False)
    budget_amount = db.Column(db.Integer, nullable=False)
    budget_frequency = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    # user = db.relationship("User", backref="users")
    category_id = db.Column(db.Integer, db.ForeignKey(Categories.category_id))
    
    # category = db.relationship("category", backref="categories")
    
    def __repr__(self):
        return f'<Budget user_id={self.user_id} budget_id={self.budget_id} category_id={self.category_id} budget_name={self.budget_name} budget_description={self.budget_description} budget_amount={self.budget_amount}'

class Advice(db.Model):
    """ Advice model """
    __tablename__ = "advice"
    advice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    advice_name = db.Column(db.String, nullable=False, unique=True)
    advice_description = db.Column(db.String, nullable=False)
    advice_price = db.Column(db.Integer, nullable=False)
    advice_img = db.Column(db.String)
    advice_info_id = db.Column(db.Integer)

    budget_id = db.Column(db.Integer, db.ForeignKey(Budget.budget_id))
    category_id = db.Column(db.Integer, db.ForeignKey(Categories.category_id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    # user = db.relationship("User", backref="users")
    # category = db.relationship("category", backref="categories")
    
    def __repr__(self):
        return f'<Advice user_id={self.user_id} category_id={self.category_id} advice_name={self.advice_name} advice_price={self.advice_price} advice_description={self.advice_description} advice_img={self.advice_img} advice_info_id={self.advice_info_id}'

class User_Transactions(db.Model):
    """ User transactions model """
    __tablename__ = "user_transactions"
    user_transactions_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_transactions_name = db.Column(db.String, nullable=False, unique=True)
    user_transactions_amount = db.Column(db.Integer, nullable=False)
    user_transactions_date = db.Column(db.Date)
    user_transactions_processed = db.Column(db.Boolean, unique=False, default=True)
    budget_id = db.Column(db.Integer, db.ForeignKey(Budget.budget_id))
    category_id = db.Column(db.Integer, db.ForeignKey(Categories.category_id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    def __repr__(self):
        return f'<User user_transactions_processed={self.user_transactions_processed} user_transactions_id={self.user_id} user_transactions_name={self.user_transactions_name} user_transactions_amount={self.user_transactions_amount} user_transactions_date={self.user_transactions_date} budget_id={self.budget_id} category_id={self.category_id}'



def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///dev_myntwise"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["CELERY_BROKER_URL"] = "sqla+postgresql://queensform@localhost/dev_myntwise"
    app.config["CELERY_BACKEND"] = "db+postgresql://localhost/dev_myntwise"
    db.app = app 
    db.init_app(app)

    if __name__ =="__main__":
       
        from server import app 

        connect_to_db(app)

        db.create_all()
        print("Connected to DB")
