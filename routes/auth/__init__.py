from flask import Blueprint

authenticator = Blueprint("auth", __name__)

from .auth import login, logout
from .utils import role_required

__all__ = ["authenticator", "login", "logout", "role_required"]