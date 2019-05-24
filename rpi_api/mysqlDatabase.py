"""
mysql.py

Connect to a MySQL database.
"""

import mysql.connector
from mysql.connector import errorcode
import logging

# Logging and debugging
LOGGER = logging.getLogger(__name__)
DEBUG = True

#from simhome.utils.custom_logger import make_logger

#LOGGER = make_logger(__name__)


class DatabaseConnectionError(Exception):
    """"""
    pass


class DatabaseConnection:
    """
    Connect to a MySQL database.
    Support for context management and standard MySQL operations.
    """

    def __init__(self, db_config: dict):
        """
        Attempts to connect to database with configuration.

        List of configuration arguments:
        https://dev.mysql.com/doc/connector-python/en/connector-python
        -connectargs.html

        :param db_config: database connection configuration
        """
        LOGGER.debug("Creating new instance of DatabaseConnection...")
        try:
            self._connection = mysql.connector.connect(**db_config)
            self._cursor = self._connection.cursor()
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Something is wrong with your user name or password"
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database does not exist"
            else:
                message = error
            LOGGER.error(message)
            raise DatabaseConnectionError(message)
        LOGGER.debug("Successfully connected!")

    def __enter__(self) -> "DatabaseConnection":
        """Return the MySQLDatabaseConnection when entering context."""
        return self

    def __exit__(self, exec_type, exec_val, exec_tb) -> None:
        """Close the connection when exiting context."""
        self.close()

    @property
    def connection(self) -> mysql.connector.connection.MySQLConnection:
        """Return the connection to the database."""
        return self._connection

    @property
    def cursor(self) -> mysql.connector.cursor.MySQLCursor:
        """Return the cursor in the database."""
        return self._cursor

    @property
    def database(self) -> str:
        """Return the name of the target database."""
        query = "SELECT DATABASE()"
        LOGGER.debug(query)
        self._cursor.execute(query)
        return self._cursor.fetchone()[0]

    @database.setter
    def database(self, value: str):
        """
        Change the target database.
        :param value: name of database to switch to
        """
        query = "USE {database}".format(database = value)
        LOGGER.debug(query)
        try:
            self._cursor.execute(query)
        except Exception as error:
            LOGGER.error(error)
            raise DatabaseConnectionError(error)

    def execute(self, value: dict):
        """Insert Value into database
            :param value: tuple of ledPin and ledState"""
        ledPin = value["led_pin"]
        ledState = 0
        if value["state"] == False: ledState = 0
        else: ledState = 1
        query = "INSERT INTO pinValues(pinNumber, pinState) VALUES('{}', '{}');".format(ledPin, ledState)
        LOGGER.debug("Inserted ledPin '{}' with state '{}' into the database".format(ledPin, ledState))
        cursor = self._cursor
        cursor.execute(query)
        self.commit()
    

    def commit(self) -> None:
        """Commit current transaction."""
        LOGGER.debug("Committing...")
        self._connection.commit()
        LOGGER.debug("Committed!")

    def rollback(self) -> None:
        """Rollback transaction."""
        LOGGER.debug("Rolling back...")
        self._connection.rollback()
        LOGGER.debug("Rolled back!")

    def close(self) -> None:
        """Close connection to database."""
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
            LOGGER.debug("Database connection closed")