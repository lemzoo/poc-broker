import logging
from broker.broker_exception import ConnectionNotOpenedYet
from broker.broker_exception import ChannelDoesntExist


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ChannelHandler(object):
    """This is a  Connection Handler to manage the connection between the
    client and RabbitMQ.

    """

    def __init__(self, connection):
        self._connection = connection
        self._channel = None
        # self.open_channel()

    def open_channel(self):
        """Open a Channel by using the connection. This channel allow the
        producer to push the message to RabbitMQ.
        """
        LOGGER.info('Opening channel for the producer')
        # Check the connection
        if self._connection is None:
            raise ConnectionNotOpenedYet('The connection is not opened')
        self._channel = self._connection.channel()

    def close_channel(self):
        """Close the channel after its use. NB : The channel is a lightwise
        ressource for RabbitMQ.
        """
        print('The channel will close in a few time')
        self._channel.close()

    def get_channel(self):
        """Get the current opened connection """
        if self._channel is None:
            raise ChannelDoesntExist('The channel doesn''t exist yet')
        return self._channel
