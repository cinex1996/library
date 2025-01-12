from flask import Blueprint, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app import db  # Import db from the app setup
from app.models.users import Users, Books

login = Blueprint("login", __name__, template_folder="templates")
register = Blueprint("register", __name__, template_folder="templates")
log_out = Blueprint("logout", __name__, template_folder="templates")
books = Blueprint("books", __name__, template_folder="templates")


@login.route("/")
def index():
    return render_template("login.html")


@login.route("/login", methods=["POST", "GET"])
def login_users():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        found_user = Users.query.filter_by(email=email).first()
        if not email or not password:
            flash("Pola są puste", "error")
            return render_template("login.html")
        # Add login logic here, e.g., verify user credentials
        if not found_user:
            flash("Taki użytkownik nie istnieje w serwisie", "error")
            return render_template("login.html")
        if not check_password_hash(found_user.password, password):
            flash("Podałeś złe hasło do swojego konta", "error")
            return render_template("login.html")
        session['email'] = email
        flash("Udało ci się zalogować do swojego konta", "succes")
        users = Books.query.all()
        return render_template("homepage.html", users=users)

    return render_template("login.html")


@register.route("/register", methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        answer = request.form.get("answer")

        # Validate all fields are filled
        if not email or not password or not repeat_password or not answer:
            flash("Wszystkie pola muszą być uzupełnione", "error")
            return render_template("register.html")

        # Check if passwords match
        if password != repeat_password:
            flash("Hasła muszą się zgadzać", "error")
            return render_template("register.html")

        # Check if email already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email jest już zarejestrowany", "error")
            return render_template("register.html")

        # Hash password and answer
        try:
            hashed_password = generate_password_hash(password)
            hash_answer = generate_password_hash(answer)

            # Save new user to the database

            user = Users(email=email, password=hashed_password, answer=hash_answer)
            db.session.add(user)
            db.session.commit()

            flash("Rejestracja zakończona sukcesem! Możesz się zalogować.", "success")
            return redirect(url_for("login.index"))

        except Exception as e:
            flash("Wystąpił błąd podczas rejestracji. Spróbuj ponownie.", "error")
            print(f"Error: {e}")  # For debugging purposes only
            return render_template("register.html")

    return render_template("register.html")


@register.route("/change_password", methods=["POST", "GET"])
def change_password():
    # Jeśli nie, przekierowanie do logowania

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        answer = request.form.get('answer')

        # Weryfikacja, czy wszystkie pola są wypełnione
        if not email or not password or not repeat_password or not answer:
            flash("Wszystkie pola muszą być uzupełnione", "error")
            return render_template("change_password.html")

        # Weryfikacja, czy hasła się zgadzają
        if password != repeat_password:
            flash("Hasła muszą się zgadzać", "error")
            return render_template("change_password.html")

        # Szukamy użytkownika w bazie
        found_user = Users.query.filter_by(email=email).first()

        if not found_user:
            flash("Nie ma takiego użytkownika o takiej nazwie", "error")
            return render_template("change_password.html")

        # Weryfikacja odpowiedzi na pytanie zabezpieczające
        if not check_password_hash(found_user.answer, answer):
            flash("Podałeś złą odpowiedź", "error")
            return render_template("change_password.html")

        # Haszowanie nowego hasła
        new_hashed_password = generate_password_hash(password)
        found_user.password = new_hashed_password

        try:
            db.session.commit()  # Zapisz zmiany w bazie
            flash("Hasło zostało zmienione", "success")
            return redirect(url_for("index"))  # Po udanej zmianie hasła, przekierowanie na stronę główną
        except Exception:
            db.session.rollback()  # W przypadku błędu, wycofaj zmiany
            flash("Coś poszło nie tak", "error")
            return render_template("change_password.html")

    return render_template("change_password.html")


@log_out.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login.login_users'))


@books.route("/add_books", methods=["POST", "GET"])
def add_books():
    if request.method == "POST":
        name_books = request.form.get("name_book")
        gerne = request.form.get("gerne")
        books = Books(name_book=name_books, gerne=gerne,user=session['email'])
        db.session.add(books)
        db.session.commit()
        return render_template("addbooks.html")

    return render_template("addbooks.html")


@books.route("/view_book", methods=["POST", "GET"])
def view_books():
    users = Books.query.filter(Books.user==session['email']).all()
    return render_template("homepage.html", users=users)
