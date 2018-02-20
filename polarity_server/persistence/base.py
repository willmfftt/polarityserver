class BasePersistence:

    OS_FAMILY = []

    def __init__(self, host, user):
        self._host = host
        self._user = user

    def install(self):
        raise NotImplementedError
