from flask import Blueprint

admin = Blueprint("admin", __name__)

from .dashboard import dashboard

__all__ = [
    "admin",
    "dashboard",
]