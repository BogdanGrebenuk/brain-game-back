from marshmallow import (Schema, fields, validate)

from app.user.domain.role import UserRole


class CreateUserSchema(Schema):
    id = fields.String(required=True)
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    patronymic = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1))
    role = fields.String(required=True, validate=validate.OneOf(UserRole.get_roles()))


class AuthenticateUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1))
