from app import db


class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60), unique=True)
    answer = db.Column(db.String(60), unique=True)

    def __init__(self, email, password, answer):
        self.email = email
        self.password = password
        self.answer = answer


class Books(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name_book = db.Column(db.String(60))
    gerne = db.Column(db.String(60))
    user=db.Column(db.String(60))

    def __init__(self, name_book, gerne,user):
        self.name_book = name_book
        self.gerne = gerne
        self.user = user
