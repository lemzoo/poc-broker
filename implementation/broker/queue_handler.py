import pika
import logging
from broker.rabbit_api import list_queues
from broker.broker_exception import ChannelDoesntExist
from broker.broker_exception import QueueNameDoesntMatch
from broker.broker_exception import ExchangeNotDefinedYet
from broker.broker_exception import BasicPropertiesIsNotSet


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class QueueHandler(object):
    """This is an Exchange Handler which use the channel handler to set a new
    or default exchange in RabbitMQ.

    """

    def __init__(self, channel, exchange_name):
        """Create a new instance of exchange handler class by using the channel.

        :param ChannelHandler channel: The given channel to connect to RabbitMQ
        :param str exchange_name : The name of the exchange to set
        """
        self._channel = channel
        self._exchange = exchange_name
        self._properties = None

    def _check_basic_config(self):
        if self._channel is None:
            raise ChannelDoesntExist('Channel is not defined yet')

        if self._exchange is None:
            raise ExchangeNotDefinedYet('The exchange is not defined')

        return

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

    def get_basic_properties(self):
        if self._properties is None:
            raise BasicPropertiesIsNotSet('The basic properties is not defined\
                Please define it by calling setup_properties')
        return self._properties

    def setup_queue(self, queue_name):
        """Setting the queue to allow pushong in a specied exchange

        :param str queue_name : The name of the queue to set in RabbitMQ.
        """
        LOGGER.info('Setting the queue `%s` and bind it to the default\
                    exchange `%s`', queue_name, self._exchange)

        # Check if the channel is set or not
        self._check_basic_config()

        # Create the queue
        declared_queue = self.create_queue(queue_name)

        # Bind the queue to the exchange
        self.bind_queue_to_default_exchange(declared_queue)

    def create_queue(self, queue_name, durable=True, auto_delete=True):
        """Create a new queue with the arguments such as its name.

        :param str queue_name : The name of the queue to set in RabbitMQ.
        :param boolean durable : The durability of the queue in RabbitMQ.
        :param boolean auto_delete : Auto delete the queue when  the message
        are purged (No consumer/publisher working on this particular queue)
        """
        LOGGER.info('Setting the queue with this name : %s', queue_name)

        # Check the length of the queue name
        if len(queue_name) < 3:
            raise QueueNameDoesntMatch('This queue name does''nt match')

        # Check if the queue exist before creating it
        existing_queues = list_queues()
        if queue_name in existing_queues:
            return queue_name
        declared_queue = self._channel.queue_declare(queue=queue_name,
                                                     durable=durable,
                                                     auto_delete=auto_delete)
        # Check declared_queue to return the real name of the queue
        return queue_name

    def bind_queue_to_default_exchange(self, queue_name):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param str queue_name : The name of the queue to bind

        """
        self._check_basic_config()
        LOGGER.info('Binding DEFAULT_EXCHANGE to this queue `%s`', queue_name)
        self._channel.queue_bind(queue=queue_name, exchange=self._exchange)
