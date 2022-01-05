import logging
import logging.config

from assets.classes.Client import Client
from assets.classes.Queue import Queue
from assets.helpers.loaders import load_yaml_config

from flask import Flask
from flask_restful import Api

from assets.classes.api.endpoints.Lobby import Lobby
from assets.classes.api.endpoints.Status import Status

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger(__name__)

api.add_resource(Lobby, "/lobby")
api.add_resource(Status, "/status")

if __name__ == "__main__":
    # Load config and set-up logger
    config = load_yaml_config()    
    logging.config.dictConfig(config.logging)

    app.run(debug=True)

