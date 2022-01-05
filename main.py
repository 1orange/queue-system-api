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
        current_client = queue.enqueue(Client())

        return {
            'id': current_client.get_id(),
            'order_number': current_client.get_order_number(),
            'timestamp': current_client.get_iso_timestamp()
        }

class Status(Resource):
    def get(self):
        clients = queue.get_iterable()

        return {
            'Clients in queue': len(clients),
            'Clients': [
                {
                    'id': client.get_id(),
                    'order_number': client.get_order_number(),
                    'timestamp': client.get_iso_timestamp(),
                } for client in clients
            ]
        }

api.add_resource(Lobby, "/lobby")
api.add_resource(Status, "/status")


if __name__ == "__main__":
    # Load config and set-up logger
    config = load_yaml_config()    
    logging.config.dictConfig(config.logging)

    #for _ in range(15):
    #    current_client = Client()
    #    queue.enqueue(current_client)
    #queue.preview()

    app.run(debug=True)

