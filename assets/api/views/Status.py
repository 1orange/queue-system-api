from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource

from flask_restful import Resource

from ..models import QueueModel, InvalidResponseModel

from main import clients_queue


class StatusEndpoint(MethodResource, Resource):

    @doc(
        description='This endopoint is used to fetch current queue',
        tags=['Queue Status']
    )
    @marshal_with(QueueModel, code=201)
    @marshal_with(InvalidResponseModel, code=400)
    @marshal_with(InvalidResponseModel, code=404)
    @marshal_with(InvalidResponseModel, code=500)
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
