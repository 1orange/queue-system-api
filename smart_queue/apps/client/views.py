from http import HTTPStatus

from flask import Response, json, request
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource, reqparse

from smart_queue.apps.client.models import (
    ClientGETRequestModel,
    ClientPOSTRequestModel,
    InvalidResponseModel,
)
from smart_queue.db.database import get_current_client, insert_client

parser = reqparse.RequestParser()
parser.add_argument("condition_id")


class ClientEndpoint(MethodResource, Resource):
    """
    Endpoint related to clients.
    """

    @doc(description="Endpoint used for joining the queue", tags=["Client"])
    @marshal_with(ClientGETRequestModel)
    def get(self):
        """
        GET Method - Dequeue client with highest priority
        """

        client = get_current_client()

        return Response(
            response=json.dumps(
                {
                    "uuid": client.uuid,
                    "arrived": client.arrived,
                    "condition": client.condition_name,
                    "order_number": client.order_number,
                }
            ),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )

    @doc(description="Endpoint used for joining the queue", tags=["Client"])
    @use_kwargs(ClientPOSTRequestModel)
    @marshal_with(ClientGETRequestModel, code=201)
    @marshal_with(InvalidResponseModel, code=400)
    @marshal_with(InvalidResponseModel, code=404)
    @marshal_with(InvalidResponseModel, code=422)
    @marshal_with(InvalidResponseModel, code=500)
    def post(self, **kwargs):
        """
        POST Method - Enqueue client
        """

        client = insert_client(kwargs["condition_id"])

        return Response(
            response=json.dumps(
                {
                    "uuid": client.uuid,
                    "arrived": client.arrived,
                    "order_number": client.order_number,
                }
            ),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )
