import logging
from broker.broker_exception import ExchangeNameDoesntMatch
from broker.broker_exception import ChannelDoesntExist
from broker.broker_exception import ExchangeAlreadyExist
from broker.broker_exception import ExchangeNotDefinedYet


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ExchangeHandler(object):
    """This is an Exchange Handler which use the channel handler to set a new
    or default exchange in RabbitMQ.

    """

    def __init__(self, channel, exchange_name='SIAEF', type_exchange='direct',
                 durable=True, auto_delete=False):
        """Create a new instance of exchange handler class by using the channel.

        :param ChannelHandler channel: The given channel to connect to RabbitMQ
        :param str exchange_name : The name of the exchange to set
        :param str : type_exchange : The type of exchange. By default, the
        exchange is direct type to allow simple routing via the queue name.
        Here are the type of exchange : direct - fanout - topic.
        :param boolean durable : The durability of the exchange. Durable
        exchange remain active when a server restarts. Non-durable exchanges
        (transient exchanges) are purged if/when a server restarts.
        :param boolean auto_delete : Delete the exchange when all queues have
        finished using it. By default, it's False.
        """
        self._channel = channel
        self._exchange = exchange_name
        self._type = type_exchange
        self._durable = durable
        self._auto_delete = auto_delete

    def setup_exchange(self):
        """Setup or create a new exchange by using the given parameters in the
        constructor.

        """
        LOGGER.info('Setting the exchange with name :%s and type :%s',
                    self._exchange, self._type)
        if self._channel is None:
            raise ChannelDoesntExist('The channel doesn''t exist')

        if len(self._exchange) < 3:
            raise ExchangeNameDoesntMatch('This exchange name does''nt match')
        # Check if the channel doesn't exist on rabbit

        list_rabbit_exchange = []  # Correct me
        if self._exchange in list_rabbit_exchange:
            raise ExchangeAlreadyExist('This exchange is already exist')

        # Check Me : self._channel.basic_qos(prefetch_count=1)
        self._channel.exchange_declare(exchange=self._exchange,
                                       type=self._type,
                                       durable=self._durable,
                                       auto_delete=self._auto_delete)

    def get_exchange_name(self):
        """Get the current opened connection """
        LOGGER.info('Getting the exchange name')
        if self._exchange is None:
            raise ExchangeNotDefinedYet('The exchange is not defined')
        return self._exchange
