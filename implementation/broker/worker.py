# !/usr/bin/env python
import logging
from broker.channel_handler import ChannelHandler


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class Worker(object):
    """This is a  Worker that will handle a connection and queue to work
    on the available messages.
    The worker will setup the channel to use and when finished, it will also
    close the current channel.
    """

    def __init__(self, connection_handler, queue):
        """
        Instantiate a Worker with an opened connection and a queue name to work
        The channel is opened in the instantiation of the module for ready use.
        It will be closed after consuming the message on the given queue.

        :param ConnectionHandler connection : The connection to use between the
        worker and RabbitMQ.
        :param Queue queue : The name of the queue to work
        """
        self._connection = connection_handler.get_connection()
        self._queue = queue

        # 1. Setup the channel to use to publish message
        self._channel_handler = ChannelHandler(self._connection)

        # 2. Open the channel before using it
        self._channel_handler.open_channel()
        LOGGER.info('The worker on queue %s is configured successfully', queue)

    def consume_message(self):
        """Consume message on the given queue name on the constructor
        """

        # 3. Send the message via the channel
        self._channel_handler.consume_message_on_queue(self._queue)

        # 4. Close the channel after publishing the message
        self._channel_handler.close_channel()
