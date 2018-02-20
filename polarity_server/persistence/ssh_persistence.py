import os
import subprocess

from polarity_server.persistence.base import BasePersistence


class SSHPersistence(BasePersistence):

    OS_FAMILY = ["Linux"]

    def __init__(self, host, user):
        super().__init__(host, user)

    def install(self):
        SSHPersistence.__generate_ssh_key()

        if self._host.os_info.os_family in self.OS_FAMILY:
            
            return True
        return False

    @staticmethod
    def __generate_ssh_key():
        home_dir = os.environ["HOME"]
        ssh_path = "{}/.ssh/id_rsa".format(home_dir)
        if not os.path.isfile(ssh_path):
            command = [
                "ssh-keygen",
                "-f",
                ssh_path,
                "-t",
                "rsa",
                "-N",
                "",
            ]
            subprocess.Popen(command)
