import jsonpickle
from flask import Flask
from flask import request
from flask_jsonpify import jsonify

from polarity_server import PolarityServer
from polarity_server.rest.server import Server
from polarity_server.tasks.host_task import HostTask


class RestApi:

    app = Flask(__name__)
    _server = None

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
    @app.route("/hosts", methods=["POST"])
    def hosts():
        hosts = jsonpickle.decode(request.data)

        if hosts:
            for host in hosts:
                task = HostTask(host)
                PolarityServer.task_queue.put(task)

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
