from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from flask_restful import Resource

from assets.classes.Client import Client
from main import queue


class Queue(Schema):
    id = fields.Str()
    order_number = fields.Int()
    timestamp = fields.Date()

class QueueEndpoint(MethodResource, Resource):

    @doc(
        description='Endpoint used for joining the queue',
        tags=['Queue']
    )
    @marshal_with(Queue)
    def get(self):
        current_client = queue.enqueue(Client())

        return {
            'id': current_client.get_id(),
            'order_number': current_client.get_order_number(),
            'timestamp': current_client.get_iso_timestamp()
        }
