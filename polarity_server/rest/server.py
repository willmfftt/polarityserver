import logging
from threading import Thread

from werkzeug.serving import make_server


class Server(Thread):

    def __init__(self, app, port):
        super().__init__()

        logging.getLogger("werkzeug").setLevel(logging.CRITICAL)

        self._srv = make_server('127.0.0.1', port, app)
        self._ctx = app.app_context()
        self._ctx.push()

    def run(self):
        self._srv.serve_forever()

    def shutdown(self):
        self._srv.shutdown()
