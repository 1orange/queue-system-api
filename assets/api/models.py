from marshmallow import Schema, fields

class ClientGETRequestModel(Schema):
    id = fields.Str()
    order_number = fields.Int()
    timestamp = fields.Str()


class ClientPOSTRequestModel(Schema):
    id = fields.Str()


class InvalidResponseModel(Schema):
    detail = fields.Str()


class QueueModel(Schema):
    queue_size = fields.Int()
    clients = fields.Nested(
        ClientGETRequestModel(many=True)
    )