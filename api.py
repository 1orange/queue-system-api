from main import logger

from assets.classes.api.endpoints.Lobby import Lobby
from assets.classes.api.endpoints.Status import Status

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(Lobby, "/lobby")
api.add_resource(Status, "/status")

if __name__ == "__main__":
    app.run(debug=True)
