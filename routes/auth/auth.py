from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from models import User
from models.base import SessionLocal
from routes.auth.utils import redirect_authenticated_user

from . import authenticator


@authenticator.route("/login", methods=["GET"])
def login():

    if current_user.is_authenticated:
        return redirect_authenticated_user()

    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    with SessionLocal() as db_session:
        user = db_session.query(User).filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash(
            "Por favor revisa tus credenciales e intenta nuevamente.",
            "error",
        )
        return redirect(url_for("auth.login"))

    if not user.is_active:
        flash("Esta cuenta está desactivada.", "error")
        return redirect(url_for("auth.login"))

    session.clear()
    login_user(user, remember=remember)

    session["current_role"] = user.roles
    session["user_id"] = user.id
    if "admin" in session["current_role"]:
        return redirect(url_for("admin.dashboard"))


@authenticator.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
