from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    from app.views.welcome import login, register, log_out, books
    app = Flask(__name__)

    app.secret_key = "superkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mskar/PycharmProjects/library/books.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(login)  # Registers the login blueprint
    app.register_blueprint(register)
    app.register_blueprint(log_out)
    app.register_blueprint(books)

    return app