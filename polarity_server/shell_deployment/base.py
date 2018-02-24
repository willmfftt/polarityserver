class BaseShell:

    PORT = 0

    def __init__(self, host, user):
        self._host = host
        self._user = user

    def create_connection(self):
        raise NotImplementedError

    def close_connection(self):
        raise NotImplementedError

    def send_command(self, command):
        raise NotImplementedError

    def interact(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError
