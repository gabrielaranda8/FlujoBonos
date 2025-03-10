from functools import wraps

from flask import flash, redirect, session, url_for
from flask_login import current_user, login_required

from models import User
from models.base import SessionLocal
from utils.enums.user_enum import UserRoles


def refresh_session_roles():
    with SessionLocal() as db_session:
        logged_user = (
            db_session.query(User).filter_by(id=current_user.id).first()
        )
    session["current_role"] = logged_user.roles


def role_required(
    allowed_roles: list[str],
):  # TODO move to utils.validations
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            if not session.get("current_role"):
                refresh_session_roles()
            if set(allowed_roles) & set(
                session.get("current_role", [])
            ) or "admin" in session.get("current_role", []):
                return f(*args, **kwargs)
            if current_user.is_authenticated:
                flash("No tienes permiso para acceder a esta página.", "error")
                return redirect_authenticated_user()
            return redirect(url_for("auth.login"))

        return wrapper

    return decorator


def redirect_authenticated_user():
    role_list = UserRoles.list()
    for role in current_user.roles:
        if role in role_list:
            return redirect(url_for(role + ".dashboard"))