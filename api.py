from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS
from flask_restful import Api

from smart_queue.apps.client.views import ClientEndpoint
from smart_queue.apps.dashboard import static_path, templates_path
from smart_queue.apps.dashboard.routes import Dash
from smart_queue.apps.queue.views import QueueEndpoint

app = Flask(
    __name__,
    template_folder=templates_path,
    static_url_path=static_path,
    static_folder=static_path,
)
api = Api(app)

CORS(app)

app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Queue system",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0.0",
        ),
        "APISPEC_SWAGGER_URL": "/docs/json",  # URI to access API Doc JSON
        "APISPEC_SWAGGER_UI_URL": "/docs",  # URI to access UI of API Doc
    }
)

docs = FlaskApiSpec(app)

# Blueprints
app.register_blueprint(Dash)

# Endpoints
api.add_resource(ClientEndpoint, "/client")
api.add_resource(QueueEndpoint, "/queue")

# Add endpoints to swagger
docs.register(ClientEndpoint)
docs.register(QueueEndpoint)

if __name__ == "__main__":
    app.run(debug=True)
