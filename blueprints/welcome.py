from crypt import methods
from logging import error

from flask import Blueprint, render_template, request, session, url_for, flash
from sqlalchemy.testing.suite.test_reflection import users
from werkzeug.utils import redirect

from .users import Users
from . import db  # Import db from the app setup
from werkzeug.security import generate_password_hash, check_password_hash

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
        if not email or not password:
            return render_template("login.html", error="Pola nie mogą być puste")
        # Add login logic here, e.g., verify user credentials
        if not found_user:
            return render_template("login.html", error="Przykro mi taki użytkownik nie istnieje")
        if not check_password_hash(found_user.password,password):
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
        answer = request.form.get("answer")

        if not email or not password or not repeat_password or not answer:
            flash("Wszystkie pola muszą być uzupełnione","error")
            return render_template("register.html")

        if password != repeat_password:
            flash("Hasła muszą się zgadzać","error")
            return render_template("register.html")
        hash_answer = generate_password_hash(answer)
        hashed_password = generate_password_hash(password)
        with db.session.begin():# Securely hash the password
            user = Users(email=email, password=hashed_password, answer=hash_answer)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login.index"))

    return render_template("register.html")
@register.route("/change_password", methods=["POST","GET"])
def change_password():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        answer = request.form.get('answer')
        found_user = Users.query.filter_by(email=email).first()
        if not email or not password or not repeat_password or not answer:
            flash("Wszystkie pola muszą być uzupełnione","error")
            return render_template("change_password.html")
        if password != repeat_password:
            flash("Hasła się ze sobą nie zgadzają","error")
            return render_template("change_password.html")
        if not found_user:
            flash("Nie ma takiego użytkownika o takiej nazwie")
            return render_template("change_password.html")
        if not check_password_hash(found_user.answer,answer):
            flash("Podałeś złą odpowiedź", "error")
            return render_template("change_password.html")
        new_hashed_password =generate_password_hash(password)
        found_user.password = new_hashed_password
        try:
            db.session.commit()
            flash("Hało zostało zmienione","success")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            flash("Coś poszło nie tak","error")
            return render_template("change_password.html")
    return render_template("change_password.html")