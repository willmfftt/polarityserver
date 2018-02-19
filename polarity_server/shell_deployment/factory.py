from polarity_server.shell_deployment.ssh_shell import SSHShell


class ShellFactory:

    def __init__(self, host, username, password):
        self._host = host
        self._username = username
        self._password = password

    def get_shell_for_port(self, port):
        if port == SSHShell.PORT:
            return SSHShell(self._host,
                            self._username,
                            self._password)
        return None
