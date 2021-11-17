from dataclasses import dataclass


@dataclass
class CreateUserDto:
    id: str
    email: str
    password: str
    first_name: str
    last_name: str
    patronymic: str
    role: str


@dataclass
class AuthenticateUserDto:
    email: str
    password: str
