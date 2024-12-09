from flask import Blueprint, render_template, request, session
from sqlalchemy.testing.suite.test_reflection import users

from .users import Users
from . import db  # Import db from the app setup
from werkzeug.security import generate_password_hash

login = Blueprint("login", __name__, template_folder="templates")
register = Blueprint("register", __name__, template_folder="templates")


@login.route("/")
def index():
    return render_template("index.html")


@login.route("/login", methods=["POST", "GET"])
def login_users():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        found_user = Users.query.filter_by(email=email).first()
        check_password=Users.query.filter_by(password=password).first()
        if not email or not password:
            return render_template("login.html", error="Pola nie mogą być puste")
        # Add login logic here, e.g., verify user credentials
        if not found_user:
            return render_template("login.html", error="Przykro mi taki użytkownik nie istnieje")
        if password != found_user.password:
            return render_template("login.html", error="Podałeś nieprawidłowe hasło")
        session['email'] = found_user.email
        return render_template("homepage.html",succes = "Zalogowano pomyślnie")
    return render_template("login.html")


@register.route("/register", methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')

        if not email or not password or not repeat_password:
            return render_template("register.html", error="Masz gdzieś puste pola")

        if password != repeat_password:
            return render_template("register.html", error="Hasła muszą być takie same")

        hashed_password = generate_password_hash(password)  # Securely hash the password
        user = Users(email=email, password=hashed_password, repeat_password=repeat_password)

        db.session.add(user)
        db.session.commit()
        return render_template("register.html", success="Wprowadziłeś dane poprawnie")

    return render_template("register.html")