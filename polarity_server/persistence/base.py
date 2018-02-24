class BasePersistence:

    OS_FAMILY = []
    PORT = None

    def __init__(self, host, user, listen_port=None):
        self._host = host
        self._user = user
        self._listen_port = listen_port

    def install(self):
        raise NotImplementedError
