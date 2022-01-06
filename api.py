from main import logger

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from assets.api.endpoints.Queue import QueueEndpoint
from assets.api.endpoints.Status import StatusEndpoint

from flask import Flask
from flask_restful import Api
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Smart queue system',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/docs/json',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

api.add_resource(QueueEndpoint, "/queue")
api.add_resource(StatusEndpoint, "/status")

docs.register(QueueEndpoint)
docs.register(StatusEndpoint)

if __name__ == "__main__":
    app.run(debug=True)
