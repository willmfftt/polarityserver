class Session:

    def __init__(self, host, shell=None):
        self._host = host
        self._shell = shell

    @property
    def host(self):
        return self._host

    @property
    def shell(self):
        return self._shell

    @shell.setter
    def shell(self, shell):
        self._shell = shell
