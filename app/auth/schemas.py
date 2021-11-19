from marshmallow import (Schema, fields, validate)


class CreateUserSchema(Schema):
    id = fields.String(required=True)
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1))
    number = fields.Integer(required=True)


class AuthenticateUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1))
