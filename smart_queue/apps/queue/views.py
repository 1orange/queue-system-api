from http import HTTPStatus

from flask import Response, json, request
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource, reqparse

from smart_queue.apps import InvalidResponseModel
from smart_queue.apps.queue.models import (
    FoundClientsModel,
    QueuePOSTRequestModel,
)
from smart_queue.db.database import check_client_status, get_queue_status


class QueueEndpoint(MethodResource, Resource):
    """
    Endpoint related to queue.
    """

    @doc(description="Queue related endpoint", tags=["Queue"])
    # @marshal_with(ClientGETRequestModel)
    def get(self):
        """
        GET Method - Show current queue
        """

        return Response(
            response=json.dumps(
                [
                    {
                        "uuid": client.uuid,
                        "arrived": client.arrived,
                        "condition": client.condition_name,
                        "order_number": client.order_number,
                    }
                    for client in get_queue_status()
                ]
            ),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )

    @doc(description="Queue related endpoint", tags=["Queue"])
    # @use_kwargs(QueuePOSTRequestModel)
    @marshal_with(FoundClientsModel, code=200)
    @marshal_with(InvalidResponseModel, code=400)
    @marshal_with(InvalidResponseModel, code=404)
    @marshal_with(InvalidResponseModel, code=422)
    @marshal_with(InvalidResponseModel, code=500)
    def post(self):
        """
        POST Method - Check whether patient is still in queue
        """

        # NOTE: Add JSON validation

        try:
            patient_id = None

            if "uuid" in request.json:
                patient_id = request.json["uuid"]

            return Response(
                response=json.dumps(
                    {"state": check_client_status(patient_id)}
                ),
                status=HTTPStatus.OK,
                mimetype="application/json",
            )

        except KeyError:
            return Response(
                response=json.dumps({"info": "Wrong JSON format."}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )
