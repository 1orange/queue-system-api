from email.mime import application
from http import HTTPStatus

from flask import Response, json, request
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource, reqparse

from smart_queue.apps import InvalidResponseModel
from smart_queue.apps.conditions.models import (
    ConditionGETRequestModel,
    ConditionGETResponse,
    ConditionPOSTRequestModel,
)
from smart_queue.db.database import get_all_conditions, insert_condition


class ConditionEndpoint(MethodResource, Resource):
    """
    Endpoint related to queue.
    """

    @doc(description="Endpoint used for conditions", tags=["Condition"])
    # @marshal_with(ConditionGETResponse)
    @marshal_with(InvalidResponseModel, code=400)
    @marshal_with(InvalidResponseModel, code=404)
    @marshal_with(InvalidResponseModel, code=422)
    @marshal_with(InvalidResponseModel, code=500)
    def get(self):
        """
        GET Method - Get all condtions
        """

        return Response(
            response=json.dumps(
                [
                    {
                        "id": condition.id,
                        "name": condition.name,
                        "description": condition.description,
                    }
                    for condition in get_all_conditions()
                ]
            ),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )

    @doc(description="Endpoint used for conditions", tags=["Condition"])
    # @use_kwargs(ConditionPOSTRequestModel)
    @marshal_with(ConditionPOSTRequestModel, code=201)
    @marshal_with(InvalidResponseModel, code=400)
    @marshal_with(InvalidResponseModel, code=404)
    @marshal_with(InvalidResponseModel, code=422)
    @marshal_with(InvalidResponseModel, code=500)
    def post(self):
        """
        POST Method - Insert new condition
        """

        # NOTE: Add JSON validation

        try:
            name = None
            desc = None

            if "name" in request.json:
                name = request.json["name"]

            if "description" in request.json:
                desc = request.json["description"]

            # Add condition
            insert_condition(name, desc)

        except KeyError:
            return Response(
                response=json.dumps({"info": "Wrong JSON format."}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )
