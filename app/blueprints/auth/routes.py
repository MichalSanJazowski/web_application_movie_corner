from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ...extensions import db
from ...models import User
from ...forms import LoginForm, RegisterForm
from . import auth_bp

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("auth.login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("auth.login"))
        else:
            login_user(user)
            return redirect(url_for("main.home"))
    return render_template("login.html", form=form, current_user=current_user)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if existing:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("auth.signup"))

        hash_pw = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
        new_user = User(email=form.email.data, name=form.name.data, password=hash_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.home"))
    return render_template("signup.html", form=form, current_user=current_user)

@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("main.home"))
