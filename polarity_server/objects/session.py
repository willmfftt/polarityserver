class Session:

    def __init__(self, host, user, shell=None, listen_port=None):
        self._host = host
        self._user = user
        self._shell = shell
        self._listen_port = listen_port

    @property
    def host(self):
        return self._host

    @property
    def username(self):
        return self._user.username

    @property
    def shell(self):
        return self._shell

    @shell.setter
    def shell(self, shell):
        self._shell = shell

    @property
    def listen_port(self):
        return self._listen_port

    @listen_port.setter
    def listen_port(self, listen_port):
        self._listen_port = listen_port
