class BaseShell:

    PORT = 0

    def __init__(self, host, username,
                 password=None):
        self._host = host
        self._username = username
        self._password = password

    def create_connection(self):
        raise NotImplementedError

    def close_connection(self):
        raise NotImplementedError

    def interact(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError
