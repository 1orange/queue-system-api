from marshmallow import Schema, fields


class ConditionGETRequestModel(Schema):
    description = fields.Str()
    id = fields.Int()
    name = fields.Str()


class ConditionPOSTRequestModel(Schema):
    name = fields.Str()
    description = fields.Str()


class ConditionGETResponse(Schema):
    conditions = fields.Nested(ConditionGETRequestModel(many=True))
