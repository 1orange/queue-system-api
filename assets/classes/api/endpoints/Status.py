from flask_restful import Resource

from main import queue


class Status(Resource):
    def get(self):
        clients = queue.get_iterable()

        print(hex(id(queue)))

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
