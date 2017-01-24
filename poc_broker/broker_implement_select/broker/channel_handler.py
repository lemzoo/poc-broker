# -*- coding: utf-8 -*-

import logging

from broker.broker_exception import ChannelIsAlreadyInUse
from broker.broker_exception import ConnectionIsOffline

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ChannelHandler(object):
    """This is an example publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    It uses delivery confirmations and illustrates one way to keep track of
    messages that have been sent and if they've been confirmed by RabbitMQ.

    """

    def __init__(self):
        """Setup the example publisher object, passing in the URL we will use
        to connect to RabbitMQ.

        :param str amqp_url: The URL for connecting to RabbitMQ

        """
        self._connection = None
        self._channel = None

    def create_new_channel(self, connection):
        """Create a new Channel by using the handler connection.
        Before openning the connection, check if it's opened or not.
        If not, open the connection and return it.
        """

        # Get the opened connection
        self._connection = connection
        # Connection is not opened
        if self._connection is None:
            LOGGER.warning('Connection Handler is not openned')
            raise ConnectionIsOffline('Connection to the server is not opened')

        # Channel is already in use
        if self._channel is not None:
            LOGGER.warning('Channel Handler is already in use')
            raise ChannelIsAlreadyInUse('Channel Handler is already in use')

        # Create new channel
        self.open_channel()
        return self._channel

    def open_channel(self):
        import pdb; pdb.set_trace()
        """This method will open a new channel with RabbitMQ by issuing the
        Channel.Open RPC command. When RabbitMQ confirms the channel is open
        by sending the Channel.OpenOK RPC reply, the on_channel_open method
        will be invoked.

        """
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        import pdb; pdb.set_trace()
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        # self.open_channel_to_use()

    def add_on_channel_close_callback(self):
        import pdb; pdb.set_trace()
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        import pdb; pdb.set_trace()
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        LOGGER.warning('Channel was closed: (%s) %s', reply_code, reply_text)
        self._channel = None

    def open_channel_to_use(self):
        # self._channel.
        pass

    def close_channel(self):
        import pdb; pdb.set_trace()
        """Invoke this command to close the channel with RabbitMQ by sending
        the Channel.Close RPC command.

        """
        if self._channel is not None:
            LOGGER.info('Closing the channel')
            self._channel.close()
