# -*- coding: utf-8 -*-

import logging

from broker.broker_exception import ExchangeNotDefinedYet
from broker.broker_exception import ExchangeAlreadyInUse
from broker.broker_exception import ChannelDoesntExist

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ExchangeHandler(object):
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
        self._channel = None
        self._exchange = None

    def create_exchange(self, channel, exchange_name):
        """Create an exchange to use. This exchange is set only one time during
        the execution of the Broker. The exchange is 'direct' type now. In the
        future, we can enhance this to perform the broker.

        :param exchange_name: The name of the exchange

        """
        LOGGER.info('Create a new exchange')
        if self._channel is None:
            LOGGER.warning('The channel is not exist')
            raise ChannelDoesntExist('The channel is not exist')

        if self._exchange is not None:
            LOGGER.warning('This exchange is already exist')
            raise ExchangeAlreadyInUse('This exchange is already exist')

        self._exchange = exchange_name
        self.setup_exchange(self._exchange)

        return self.get_exchange_name()

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        LOGGER.info('Declaring exchange %s', exchange_name)
        # Check if the exchange exist on rabbit or not
        exchange_list = []
        if exchange_name in exchange_list:
            raise ExchangeAlreadyInUse('This exchange exists on the server')

        self._channel.basic_qos(prefetch_count=1)
        self._channel.exchange_declare(callback=None,
                                       exchange=exchange_name,
                                       type=self.EXCHANGE_TYPE)

    def get_exchange_name(self):
        if self._exchange is None:
            LOGGER.warning('No Exchange defined yet')
            raise ExchangeNotDefinedYet('No Exchange defined yet')
        return self._exchange
