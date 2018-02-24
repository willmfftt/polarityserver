import os

from polarity_server.shell_deployment.ssh_shell import SSHShell


class ShellFactory:

    def __init__(self, host, user):
        self._host = host
        self._user = user

    def get_shell_for_port(self, port, use_priv_ssh_key=False):
        if port == SSHShell.PORT:
            priv_ssh_key = None

            if use_priv_ssh_key:
                home_dir = os.environ["HOME"]
                priv_ssh_key = "{}/.ssh/id_rsa".format(home_dir)

            return SSHShell(self._host, self._user, priv_ssh_key)
        return None
