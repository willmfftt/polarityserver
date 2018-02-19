from queue import Empty
from queue import Queue

from flask import Flask
from flask import request
from flask_jsonpify import jsonify

from polarity_server.rest.server import Server
from polarity_server.tasks import ShellTask


class RestApi:

    app = Flask(__name__)
    _server = None
    _task_queue = Queue()

    @staticmethod
    def start_server(port):
        if not RestApi._server:
            RestApi._server = Server(RestApi.app, port)
            RestApi._server.start()

    @staticmethod
    def stop_server():
        if RestApi._server:
            RestApi._server.shutdown()
            RestApi._server = None

    @staticmethod
    @app.route("/shell/<host>", methods=["POST"])
    def shell(host):
        data = request.get_json()

        if "username" not in data:
            return RestApi.failure_response("Missing username")
        if "password" not in data:
            return RestApi.failure_response("Missing password")
        if "port" not in data:
            return RestApi.failure_response("Missing port")

        task = ShellTask(host, data["username"],
                         data["password"], int(data["port"]))
        RestApi._task_queue.put(task)

        return RestApi.success_response()

    @staticmethod
    def success_response(message=None):
        response_data = {"success": True}

        if message:
            response_data.update({"message": message})

        return jsonify(response_data)

    @staticmethod
    def failure_response(message=None):
        response_data = {"success": False}

        if message:
            response_data.update({"message": message})

        return jsonify(response_data)

    @staticmethod
    def get_task():
        try:
            return RestApi._task_queue.get(timeout=1.0)
        except Empty:
            return None
