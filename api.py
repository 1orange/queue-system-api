from main import logger

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from assets.api.endpoints.Client import ClientEndpoint
from assets.api.endpoints.Status import StatusEndpoint

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
api = Api(app)

CORS(app)

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

# Create endpoint route
api.add_resource(ClientEndpoint, "/client")
api.add_resource(StatusEndpoint, "/status")

# Add endpoints to swagger
docs.register(ClientEndpoint)
docs.register(StatusEndpoint)

if __name__ == "__main__":
    app.run(debug=True)
