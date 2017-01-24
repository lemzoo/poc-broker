# !/usr/bin/env python
import logging
import pika
import json
from broker.rabbit_api import get_all_queue
from broker.broker_exception import QueueNameDoesntMatch
from broker.broker_exception import ExchangeNameDoesntMatch
from broker.broker_exception import ChannelDoesntExist
from broker.broker_exception import ConnectionNotOpenedYet
from broker.channel_handler import ChannelHandler


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
        self.setup_properties()
        self.setup_exchange()

    def setup_properties(self, app_id='ANEF-SIEF',
                         content_type='application/json',
                         delivery_mode=2):
        """Set the basic properties for RabbitMQ.

        :param str app_id : The id of the current app.
        :param str content_type : The content type of the message
        :param int delivery_mode : The delivering mode for RabbitMQ. `2` means
        the message will be persisted on the disk and `1` means the message
        will not be persisted.
        """
        LOGGER.info('Setting the properties for RabbitMQ')
        self._properties = pika.BasicProperties(app_id=app_id,
                                                content_type=content_type,
                                                delivery_mode=delivery_mode)

    def setup_exchange(self, exchange_name=DEFAULT_EXCHANGE, type='direct'):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the process to setup the queue can start.

        :param str exchange_name: The name of the exchange to declare
        :param type : The type of the exchange to setup. By default, the
        the exchange is direct type.

        """
        # Open the channel for the first time to setup the exchange
        channel_handler = ChannelHandler(self._connection)
        channel_handler.open_channel()
        self._channel = channel_handler.get_channel()
        LOGGER.info('Setting the exchange with this name : %s', exchange_name)
        if len(exchange_name) < 3:
            raise ExchangeNameDoesntMatch('This exchange name does''nt match')

        # Check Me : self._channel.basic_qos(prefetch_count=1)
        self._channel.exchange_declare(exchange=exchange_name, type=type)

        # Close the channel after setting the exchange
        # self._channel.close_channel()
        channel_handler.close_channel()

    def bind_queue_to_exchange(self, queue_name, exchange_name):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        LOGGER.info('Binding DEFAULT_EXCHANGE to this queue `%s`', queue_name)
        self._channel.queue_bind(queue=queue_name, exchange=exchange_name)

    def setup_queue(self, queue_name, exchange_name=DEFAULT_EXCHANGE):
        """Setting the queue to allow pushong in a specied exchange

        :param str queue_name : The name of the queue to set in RabbitMQ.
        :param str exchange_name : The name of the exchange.
        """
        LOGGER.info('Setting the queue `%s` and bind it to the default\
                    exchange `%s`', queue_name, exchange_name)
        # Check if the channel is set or not
        if self._channel is None:
            raise ChannelDoesntExist('The channel doesn''t exist')

        # Create the queue
        self.create_queue(queue_name)

        # Bind the queue to the exchange
        self.bind_queue_to_exchange(queue_name, exchange_name)

    def create_queue(self, queue_name, durable=True, auto_delete=True):
        """Create a new queue with the arguments such as its name.

        :param str queue_name : The name of the queue to set in RabbitMQ.
        :param boolean durable : The durability of the queue in RabbitMQ.
        :param boolean auto_delete : Auto delete the queue when  the message
        are purged (No consumer/publisher working on this particular queue)
        """
        LOGGER.info('Setting the queue with this name : %s', queue_name)
        # Check if the channel is set or not
        if self._channel is None:
            raise ChannelDoesntExist('The channel doesn''t exist')

        # Check the length of the queue name
        if len(queue_name) < 3:
            raise QueueNameDoesntMatch('This queue name does''nt match')

        self._channel.queue_declare(queue=queue_name,
                                    durable=durable,
                                    auto_delete=auto_delete)

    def publish(self, queue='hello', message={'Hello World !'}):
        """Publish the given message in the given queue

        :param str queue : The queue name which to publish the given message
        :param dict message : The message to publish in RabbitMQ
        """
        # 2. Get a channel
        # Open the channel for the first time to setup the exchange
        channel_handler = ChannelHandler(self._connection)
        channel_handler.open_channel()
        self._channel = channel_handler.get_channel()
        # 3. Get all existing queues and check if the queue args exists
        queues = get_all_queue(self._host, 15672,
                               self._user_id, self._password)
        # 4. Check if the queue exists or not in rabbit.
        if queue not in queues:
            # If the queue does'nt exist, setup the queue
            self.setup_queue(queue)
        # 5. The after, send the message
        self._channel.basic_publish(exchange=DEFAULT_EXCHANGE,
                                    routing_key=queue,
                                    body=json.dumps(message),
                                    properties=self._properties)
        # 6. Close the channel
        channel_handler.close_channel()
        LOGGER.info('Bellow message `%s` is published in `%s`', message, queue)
