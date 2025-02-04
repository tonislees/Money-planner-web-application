from datetime import datetime, timedelta, timezone
from authlib.jose import jwt
from rahaleht import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    expenses = db.relationship('Expense', backref='owner', lazy=True)
    subcategory = db.relationship('Subcategory', backref='owner', lazy=True)
    
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
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Expense('{self.money}', '{self.category}', '{self.subcategory} '{self.description}', '{self.date}')"


class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Expense('{self.money}', '{self.category}', '{self.subcategory} '{self.description}', '{self.date}')"