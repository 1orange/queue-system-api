from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from flask_restful import Resource

from .Queue import Queue

from main import queue


class Status(Schema):
    queue_size = fields.Int()
    clients = fields.Nested(
        Queue
    )

class StatusEndpoint(MethodResource, Resource):

    @doc(
        description='This endopoint is used to fetch current queue',
        tags=['Lobby']
    )
    @marshal_with(Status)
    def get(self):
        clients = queue.get_iterable()

        return {
            'queue_size': len(clients),
            'clients': [
                {
                    'id': client.get_id(),
                    'order_number': client.get_order_number(),
                    'timestamp': client.get_iso_timestamp(),
                } for client in clients
            ]
        }
