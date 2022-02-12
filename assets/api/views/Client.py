from ast import parse
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from flask_restful import Resource, reqparse

from assets.classes.ClientClass import Client
from ..models import ClientGETRequestModel, ClientPOSTRequestModel, InvalidResponseModel

from main import clients_queue


parser = reqparse.RequestParser()
parser.add_argument('id')


class ClientEndpoint(MethodResource, Resource):
    """
    Endpoint related to clients.
    """
    @doc(
        description='Endpoint used for joining the queue',
        tags=['Client']
    )
    @marshal_with(ClientGETRequestModel)
    def get(self):
        """
        GET Method - Endpoint used to add client in to the queue.
        """
        current_client = clients_queue.enqueue(Client())

        return {
            'id': current_client.get_id(),
            'order_number': current_client.get_order_number(),
            'timestamp': current_client.get_iso_timestamp()
        }
    
    @doc(
        description='Endpoint used for joining the queue',
        tags=['Client']
    )
    @use_kwargs(ClientPOSTRequestModel)
    @marshal_with(ClientGETRequestModel, code=201)
    @marshal_with(InvalidResponseModel, code=400)
    @marshal_with(InvalidResponseModel, code=404)
    @marshal_with(InvalidResponseModel, code=500)
    def post(self, **kwargs):
        """
        POST Method - Endpoint used to get info about specific client.

        REQUEST JSON:
        {
            id: str
        }
        """

        try:
            client = clients_queue.find_client_by_id(kwargs['id'])

            return {
                'id': client.get_id(),
                'order_number': client.get_order_number(),
                'timestamp': client.get_iso_timestamp()
            }
      
        except Exception as error:
            print(error)
            return {
                'reason': 'Wrong json format'
            }
