from flask_restful import Resource

from assets.classes.Client import Client
from main import queue

class Lobby(Resource):
    def get(self):
        current_client = queue.enqueue(Client())

        return {
            'id': current_client.get_id(),
            'order_number': current_client.get_order_number(),
            'timestamp': current_client.get_iso_timestamp()
        }