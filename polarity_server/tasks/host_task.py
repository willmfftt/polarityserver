from polarity_server.objects import Session
from polarity_server.persistence import PersistenceFactory
from polarity_server.shell_deployment import ShellFactory


class HostTask:

    def __init__(self, host, shared_users=None):
        self._host = host
        self._shared_users = shared_users

    def execute(self):
        sessions = []
        listen_port = 10000

        ports = []
        for port in self._host.ports:
            ports.append(port.port)

        if self._shared_users:
            for user in self._shared_users:
                PersistenceFactory.install(self._host,
                                           user, listen_port)
                for port in ports:
                    factory = ShellFactory(self._host, user)
                    shell = factory.get_shell_for_port(port, True)
                    if shell:
                        session = Session(self._host, user,
                                          shell, listen_port)
                        sessions.append(session)

                listen_port += 1

        if sessions:
            return {self._host.ip_address: sessions}

        return {}
