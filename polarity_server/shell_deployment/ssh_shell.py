import logging
import time

from pexpect.pxssh import ExceptionPxssh
from pexpect.pxssh import pxssh

from polarity_server.shell_deployment.base import BaseShell


class SSHShell(BaseShell):

    PORT = 22

    def __init__(self, host, user, priv_key_path=None):
        super().__init__(host, user)

        self._priv_key_path = priv_key_path
        self._conn = None

    def create_connection(self):
        if self._conn and self._conn.isalive():
            logging.info("SSH connection already established to host %s",
                         self._host.ip_address)
            return False

        try:
            tmp_conn = pxssh()

            if self._priv_key_path:
                tmp_conn.login(self._host.ip_address, self._user.username,
                               ssh_key=self._priv_key_path)
            elif self._user.password:
                tmp_conn.login(self._host.ip_address, self._user.username,
                               self._user.password)
            else:
                logging.warning("Not enough information to open "
                                "SSH connection for host %s", self._host.ip_address)
                return False

            self._conn = tmp_conn
            self._conn.sendline("/bin/bash")

            logging.info("SSH connection established to host %s",
                         self._host.ip_address)

            return True
        except ExceptionPxssh:
            logging.warning("SSH connection failed to host %s",
                            self._host.ip_address)
            return False

    def close_connection(self):
        if self._conn:
            logging.info("Closing SSH connection on host %s", self._host.ip_address)
            self._conn.close()

    def send_command(self, command):
        if self.is_alive():
            self._conn.sendline(command)
            time.sleep(0.5)

    def interact(self):
        if self.is_alive():
            logging.info("Interacting with SSH shell on host %s. "
                         "Use ^] to escape shell without exiting", self._host.ip_address)
            time.sleep(2)
            self._conn.sendline("clear")
            self._conn.interact()
        else:
            logging.info("Cannot interact with SSH connection. "
                         "Connection to host %s closed", self._host.ip_address)

    def is_alive(self):
        return self._conn and self._conn.isalive()
