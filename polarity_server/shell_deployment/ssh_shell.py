import logging
import time

from pexpect.pxssh import ExceptionPxssh
from pexpect.pxssh import pxssh

from polarity_server.shell_deployment.base import BaseShell


class SSHShell(BaseShell):

    PORT = 22

    def __init__(self, host, username, password=None,
                 priv_key_path=None):
        super().__init__(host, username, password)

        self._priv_key_path = priv_key_path
        self._conn = None

    def create_connection(self):
        if self._conn and self._conn.isalive():
            logging.info("SSH connection already established to host %s",
                         self._host)
            return False

        try:
            env_vars = {"TERM": "xterm"}

            tmp_conn = pxssh(env=env_vars)

            if self._priv_key_path:
                tmp_conn.login(self._host, self._username,
                               ssh_key=self._priv_key_path)
            elif self._password:
                tmp_conn.login(self._host, self._username,
                               self._password)
            else:
                logging.warning("Not enough information to open "
                                "SSH connection for host %s", self._host)
                return False

            self._conn = tmp_conn
            self._conn.sendline("/bin/bash")

            logging.info("SSH connection established to host %s",
                         self._host)

            return True
        except ExceptionPxssh:
            logging.warning("SSH connection failed to host %s",
                            self._host)
            return False

    def close_connection(self):
        if self._conn:
            logging.info("Closing SSH connection on host %s", self._host)
            self._conn.close()

    def interact(self):
        if self._conn and self._conn.isalive():
            logging.info("Interacting with SSH shell on host %s. "
                         "Use ^] to escape shell without exiting", self._host)
            time.sleep(2)
            self._conn.sendline("clear")
            self._conn.interact()
        else:
            logging.info("Cannot interact with SSH connection. "
                         "Connection to host %s closed", self._host)

    def is_alive(self):
        return self._conn and self._conn.isalive()
