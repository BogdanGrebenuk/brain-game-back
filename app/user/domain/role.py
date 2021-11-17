from enum import Enum


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'

    @classmethod
    def get_roles(cls):
        return [i.value for i in cls]
