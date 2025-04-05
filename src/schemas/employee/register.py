from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.String(required=True, validate=validate.Length(min=8, max=16))
    name = fields.String(required=True, validate=validate.Length(max=120))
    family_name = fields.String(required=True, validate=validate.Length(max=120))