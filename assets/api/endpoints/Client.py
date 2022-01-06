from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from flask_restful import Resource

from assets.classes.ClientClass import Client
from main import clients_queue


class Client(Schema):
    id = fields.Str()
    order_number = fields.Int()
    timestamp = fields.Str()

class ClientEndpoint(MethodResource, Resource):

    @doc(
        description='Endpoint used for joining the queue',
        tags=['Client']
    )
    @marshal_with(Client)
    def get(self):
        current_client = clients_queue.enqueue(Client())

        return {
            'id': current_client.get_id(),
            'order_number': current_client.get_order_number(),
            'timestamp': current_client.get_iso_timestamp()
        }
