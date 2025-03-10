from .admin import admin
from .auth import authenticator

blueprints = [admin, authenticator]
__all__ = ["admin", "authenticator"]