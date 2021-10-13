from functools import wraps

from flask import Flask, abort, flash, session, redirect, request, render_template

from config import Config
from models import db, User
#from forms import LoginForm, RegistrationForm, ChangePasswordForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ------------------------------------------------------# Декораторы авторизации
# def login_required(f):
# (код декоратора)

# def admin_only(f):
# (код декоратора)


@app.route('/')
def render_main():
    return render_template("main.html")


@app.route('/cart/')
def render_cart():
    return render_template("cart.html")


@app.route('/account/')
def render_account():
    return render_template("account.html")


@app.route('/auth/')
def render_auth():
    return render_template("register.html")


@app.route('/register/')
def render_register():
    return render_template("register.html")


@app.route('/logout/')
def render_logout():
    return render_template("login.html")


@app.route('/ordered/')
def render_ordered():
    return render_template("ordered.html")


# ------------------------------------------------------# Страница админки
# @app.route('/')@login_required def home():
# (код страницы админки)

# ------------------------------------------------------# Страница аутентификации
# @app.route("/login", methods=["GET", "POST"])def login():
# (код страницы аутентификации)

# ------------------------------------------------------# Страница выхода из админки
# @app.route('/logout', methods=["POST"])@login_required def logout():
# (код выхода из админки)

# ------------------------------------------------------# Страница добавления пользователя
# @app.route("/registration", methods=["GET", "POST"])@admin_only@login_required def registration():
# (код страницы регистрации)

# ------------------------------------------------------# Страница смены пароля
# @app.route("/change-password", methods=["GET", "POST"])@login_required def change_password():
# (код страницы смены пароля)

if __name__ == "__main__":
    app.run()