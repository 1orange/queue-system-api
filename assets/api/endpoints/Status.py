from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from flask_restful import Resource

from .Client import Client

from main import clients_queue

class Queue(Schema):
    queue_size = fields.Int()
    clients = fields.Nested(
        Client(many=True)
    )

class StatusEndpoint(MethodResource, Resource):

    @doc(
        description='This endopoint is used to fetch current queue',
        tags=['Queue Status']
    )
    @marshal_with(Queue)
    def get(self):
        clients = clients_queue.get_iterable()

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
