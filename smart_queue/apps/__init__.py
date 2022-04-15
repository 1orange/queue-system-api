from marshmallow import Schema, fields


class InvalidResponseModel(Schema):
    detail = fields.Str()
