from ast import parse
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from flask_restful import Resource, reqparse

from assets.classes.ClientClass import Client
from main import clients_queue


parser = reqparse.RequestParser()
parser.add_argument('id')

class ClientGETRequestModel(Schema):
    id = fields.Str()
    order_number = fields.Int()
    timestamp = fields.Str()


class ClientPOSTRequestModel(Schema):
    id = fields.Str()


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
    @marshal_with(ClientGETRequestModel)
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
