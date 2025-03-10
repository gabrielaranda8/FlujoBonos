from flask_login import UserMixin, current_user
from sqlalchemy import String
from sqlalchemy.orm import Mapped, Session, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from models.base import Base
from utils.enums.user_enum import UserRoles
from utils.exeptions.user_exeptions import DeactivateCurrent


class User(UserMixin, Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    _roles: Mapped[str] = mapped_column("roles", String(120))
    is_active: Mapped[bool] = mapped_column(default=True)

    def __init__(
        self, username: str, email: str, roles: str, password: str
    ) -> None:
        self.username = username
        self.email = email
        self.roles = roles
        self.set_password(password)

    @property
    def roles(self) -> list:
        return self._roles.split(",")

    @roles.setter
    def roles(self, roles: list) -> None:
        for role in roles:
            if role not in UserRoles.list():
                raise ValueError(f"El rol {role} no es válido.")
        if "admin" not in roles and current_user.username == self.username:
            raise ValueError(
                "Solo otro administrador puede eliminar el rol admin."
            )

        self._roles = ",".join(roles)

    @roles.deleter
    def roles(self) -> None:
        self._roles = ""

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def check_email_exists(email, session: Session) -> bool:
        return session.query(User).filter_by(email=email).first() is not None

    @staticmethod
    def check_username_exists(username: str, session: Session) -> bool:
        return (
            session.query(User).filter_by(username=username).first()
            is not None
        )

    def toggle_active(self) -> None:
        if self.username == current_user.username:
            raise DeactivateCurrent("No puedes desactivar tu propia cuenta.")
        self.is_active = not self.is_active

    def delete(self, session: Session) -> None:
        if self.username == current_user.username:
            raise DeactivateCurrent("No puedes elimiar tu propia cuenta.")
        session.delete(self)

    def change_password(self, new_password: str) -> None:
        self.set_password(new_password)