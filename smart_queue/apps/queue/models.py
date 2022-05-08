import uuid

from marshmallow import Schema, fields


class QueuePOSTRequestModel(Schema):
    uuid = fields.Str()


class FoundClientsModel(Schema):
    state = fields.Str()
