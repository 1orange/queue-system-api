from marshmallow import Schema, fields


class ClientGETRequestModel(Schema):
    uuid = fields.Str()
    timestamp = fields.Str()
    condition_name = fields.Str()
    order_number = int()


class ClientPOSTRequestModel(Schema):
    condition_id = fields.Int()


class InvalidResponseModel(Schema):
    detail = fields.Str()


class QueueModel(Schema):
    queue_size = fields.Int()
    clients = fields.Nested(ClientGETRequestModel(many=True))
