class HostTask:

    def __init__(self, host, shared_users=None):
        self._host = host
        self._shared_users = shared_users

    def execute(self):
        return None
