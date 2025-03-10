from .extend_enum import ExtendedEnum


class UserRoles(ExtendedEnum):
    ADMIN = "admin"
    USER = "user"

    @classmethod
    def get_parsed(cls) -> list[str]:
        return list(map(lambda c: c.capitalize(), cls.list()))
