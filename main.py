import logging
import logging.config

from assets.classes.Client import Client
from assets.classes.Queue import Queue
from assets.helpers.loaders import load_yaml_config

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger(__name__)

queue = Queue(logger)

class Lobby(Resource):
    def get(self):
        return {'order_number': queue.enqueue(Client())}

api.add_resource(Lobby, "/lobby")


if __name__ == "__main__":
    # Load config and set-up logger
    config = load_yaml_config()    
    logging.config.dictConfig(config.logging)

    #for _ in range(15):
    #    current_client = Client()
    #    queue.enqueue(current_client)
    #queue.preview()

    app.run(debug=True)

