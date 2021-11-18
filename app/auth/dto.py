from dataclasses import dataclass


@dataclass
class CreateUserDto:
    id: str
    username: str
    email: str
    password: str
    number: int


@dataclass
class AuthenticateUserDto:
    email: str
    password: str
