from enum import unique

from werkzeug.security import generate_password_hash

from blueprints import db
class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60), unique=True)
    answer = db.Column(db.String(60), unique=True)
    def __init__(self,email,password,answer):
        self.email=email
        self.password=password
        self.answer=answer
class Books(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name_book = db.Column(db.String(60))
    gerne = db.Column(db.String(60))
    id_user = db.Column(db.Integer)
    def __init__(self,name_book,gerne,id):
        self.name_book = name_book
        self.gerne = gerne
        self.id_user = id