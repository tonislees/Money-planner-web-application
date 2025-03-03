from datetime import datetime, timedelta, timezone
from authlib.jose import jwt
from rahaleht import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def current_time():
    return datetime.now(timezone.utc) + timedelta(hours=2)

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    language = db.Column(db.String(2), nullable=False, default='en')
    last_login = db.Column(db.Date, nullable=False, default=current_time)
    expenses = db.relationship('Expense', backref='owner', lazy=True)
    budget = db.relationship('Budget', backref='owner', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        header = {"alg": "HS256"}
        payload = {
            "user_id": self.id,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_sec)
        }
        token = jwt.encode(header, payload, current_app.config['SECRET_KEY'])
        return token.decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        try:
            claims = jwt.decode(token, current_app.config['SECRET_KEY'])
            claims.validate()
            return User.query.get(claims["user_id"])
        except:
            return None

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60), nullable=False)
    subcategory = db.Column(db.String(60), nullable=False)
    money = db.Column(db.Float)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc) + timedelta(hours=2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Expense('{self.money}', '{self.category}', '{self.subcategory} '{self.description}', '{self.date}')"


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    default = db.Column(db.Boolean, nullable=False, default=False)
    month = db.Column(db.String(2), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    salary = db.Column(db.Float)
    tuition = db.Column(db.Float)
    other_incomes = db.Column(db.Float)
    rent = db.Column(db.Float)
    utilities = db.Column(db.Float)
    groceries = db.Column(db.Float)
    transport = db.Column(db.Float)
    other_living_costs = db.Column(db.Float)
    clothing = db.Column(db.Float)
    entertainment = db.Column(db.Float)
    other_personal_expenses = db.Column(db.Float)
    stocks = db.Column(db.Float)
    bonds = db.Column(db.Float)
    fonds = db.Column(db.Float)
    savings = db.Column(db.Float)
    other_investments = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Budget('{self.name}', '{self.year}', '{self.month}')"