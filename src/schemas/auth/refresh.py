from marshmallow import Schema, fields

class RefreshTokenSchema(Schema):
    refresh = fields.String(required=True, description="The refresh token")