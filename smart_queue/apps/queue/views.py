from http import HTTPStatus

from flask import Response, json
from flask_apispec import doc
from flask_apispec.views import MethodResource
from flask_restful import Resource, reqparse

from smart_queue.apps.client.models import ClientGETRequestModel
from smart_queue.db.database import get_queue_status


class QueueEndpoint(MethodResource, Resource):
    """
    Endpoint related to queue.
    """

    @doc(description="Endpoint used for joining the queue", tags=["Queue"])
    # @marshal_with(ClientGETRequestModel)
    def get(self):
        """
        GET Method - Dequeue client with highest priority
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
