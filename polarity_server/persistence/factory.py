from polarity_server.persistence.bashrc_persistence import BashRcPersistence
from polarity_server.persistence.cron_persistence import CronPersistence
from polarity_server.persistence.ssh_persistence import SSHPersistence


class PersistenceFactory:

    ORDERED_PERSISTENCE = [
        SSHPersistence,
        BashRcPersistence,
        CronPersistence,
    ]

    @classmethod
    def install(cls, host, user, listen_port=None):
        ports = []
        for port in host.ports:
            ports.append(port.port)

        for persistence_class in cls.ORDERED_PERSISTENCE:
            if persistence_class.PORT in ports:
                persistence = persistence_class(host, user, listen_port)
                persistence.install()
