"""
mysql_ssh.py
"""

from sshtunnel import SSHTunnelForwarder
import paramiko

from mysqlDatabase import (DatabaseConnection,
                                   DatabaseConnectionError)
#from simhome.utils.custom_logger import make_logger
import logging
# Logging and debugging
LOGGER = logging.getLogger(__name__)
DEBUG = True

#LOGGER = make_logger(__name__)


class SSHMySQLDatabaseConnectionError(Exception):
    pass


class DatabaseConnectionSSH(DatabaseConnection):
    """
    Connect to a MySQL Database through an SSH tunnel.
    """

    def __init__(self, db_config: dict, ssh_config: dict):
        """
        Create an SSH tunnel on the local bind address to connect to the
        database.
        """
        LOGGER.debug(
            "Creating new instance of SSHMySQLDatabaseConnection...")
        self._tunnel = SSHTunnelForwarder(**ssh_config)
        self._tunnel.start()
        LOGGER.info("Started SSH tunnel on %s:%d",
                    self._tunnel.local_bind_host,
                    self._tunnel.local_bind_port)
        try:
            super().__init__(db_config)
        except DatabaseConnectionError as error:
            self.close()
            raise SSHMySQLDatabaseConnectionError("Could not connect to MySQL database. {}".format(error))
        LOGGER.debug("Created new instance of SSHMySQLDatabaseConnection")

    def __enter__(self) -> "DatabaseConnectionSSH":
        """Return the SSHMySQLDatabaseConnection when entering context."""
        return self

    def __exit__(self, exec_type, exec_val, exec_tb) -> None:
        """Close the connection when exiting context."""
        self.close()

    def close(self) -> None:
        """Close connection to database and SSH tunnel."""
        # super().close()
        if self._tunnel is not None \
                and self._tunnel.is_active \
                and self._tunnel.is_alive:
            self._tunnel.stop()
            LOGGER.debug("Tunnel stopped")