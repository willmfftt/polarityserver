from polarity_server.objects import Session
from polarity_server.shell_deployment import ShellFactory


class ShellTask:

    def __init__(self, host, username,
                 password, port):
        self._host = host
        self._username = username
        self._password = password
        self._port = port

    def execute(self):
        factory = ShellFactory(self._host, self._username,
                               self._password)

        shell = factory.get_shell_for_port(self._port)
        if shell:
            shell.create_connection()
            session = Session(self._host, shell)
            return session

        return None
