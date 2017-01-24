# !/usr/bin/env python
import logging
from broker.channel_handler import ChannelHandler
from broker.exchange_handler import ExchangeHandler


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
DEFAULT_EXCHANGE = 'SIAEF'


class Producer(object):
    """This is a  publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    """

    def __init__(self, connection, host='localhost', port=5672,
                 user_id='guest', password='guest'):
        self._host = host
        self._port = port
        self._user_id = user_id
        self._password = password
        self._connection = connection
        self._channel = None
        self._exchange_name = None
        self.init_app()

    def init_app(self):
        """Setup the publisher object, passing in the host, port, user id and
        the password to create a parameters objects to connect to RabbitMQ.

        :param str host: The URL for connecting to RabbitMQ
        :param int port: The port which in use to connect to RabbitMQ
        :param str user_id: The user to use to get the connection with RabbitMQ
        :param password: The password for the user for authentification

        """
        LOGGER.info('Launching the init app for the producer')

        # Open channel to set the exchange
        channel_handler = ChannelHandler(self._connection)
        channel_handler.open_channel()
        self._channel = channel_handler.get_channel()

        # Set the default exchange to use
        exchange_name = 'SIEF'
        exchange_handler = ExchangeHandler(self._channel, exchange_name)
        exchange_handler.setup_exchange()
        self._exchange_name = exchange_handler.get_exchange_name()

        channel_handler.close_channel()

    def publish(self, queue, message):
        """Publish the given message in the given queue

        :param str queue : The queue name which to publish the given message
        :param dict message : The message to publish in RabbitMQ
        """
        # 1. Setup the channel to use to publish message
        channel_handler = ChannelHandler(self._connection)

        # 2. Open the channel before using it
        channel_handler.open_channel()

        # 3. Send the message via the channel
        channel_handler.send_message(self._exchange_name, queue, message)

        # 4. Close the channel after publishing the message
        channel_handler.close_channel()
        LOGGER.info('Bellow message `%s` is published in `%s`', message, queue)
