from enum import unique
from blueprints import db
class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60), unique=True)
    repeat_password = db.Column(db.String(60), unique=True)
    def __init__(self,email,password,repeat_password):
        self.email=email
        self.password=password
        self.repeat_password=repeat_password