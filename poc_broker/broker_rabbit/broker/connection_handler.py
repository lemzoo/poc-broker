
import logging
import pika

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ConnectionHandler(object):
    """This is a  Connection Handler to manage the connection between the
    client and RabbitMQ.

    """

    def __init__(self, host='localhost', port=5672,
                 user_id='guest', password='guest'):
        """Create a new instance of Connection Handler by using the given
        parameters to connect to RabbitMQ.

        :param str host: The URL for connecting to RabbitMQ
        :param int port: The port which in use to connect to RabbitMQ
        :param str user_id: The user to use to get the connection with RabbitMQ
        :param password: The password for the user for authentification
        """
        self._host = host
        self._port = port
        self._user_id = user_id
        self._password = password
        self._connection = None
        self.init_app(self._host, self._port, self._user_id, self._password)

    def init_app(self, host, port, user_id, password):
        """Setup the publisher object, passing in the host, port, user id and
        the password to create a parameters objects to connect to RabbitMQ.

        :param str host: The URL for connecting to RabbitMQ
        :param int port: The port which in use to connect to RabbitMQ
        :param str user_id: The user to use to get the connection with RabbitMQ
        :param password: The password for the user for authentification

        """
        LOGGER.info('Launching the init app for the producer')
        self.parameters = pika.ConnectionParameters(
            host, port, credentials=pika.PlainCredentials(user_id, password))
        self._connection = pika.BlockingConnection(self.parameters)

    def close_connection(self):
        """Close the connection when finishing to publish message"""
        LOGGER.info('Closing the connection for the producer')
        self._connection.close()

    def get_connection(self):
        """Get the current opened connection """
        return self._connection
