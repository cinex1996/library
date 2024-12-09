from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def create_blueprints():
    from blueprints.welcome import login, register
    app = Flask(__name__, template_folder="/home/mskar/PycharmProjects/library/templates")
    app.secret_key = "superkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mskar/PycharmProjects/library/books.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(login)  # Registers the login blueprint
    app.register_blueprint(register)
    return app