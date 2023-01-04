import os
from sqla_wrapper import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))  

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
