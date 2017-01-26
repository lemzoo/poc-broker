import logging
import json
from broker.queue_handler import QueueHandler
from broker.broker_exception import ConnectionNotOpenedYet
from broker.broker_exception import ChannelDoesntExist


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ChannelHandler(object):
    """This is a  Channel Handler which use the connection handler to get a new
    channel to allow the client to communicate with RabbitMQ.

    """

    def __init__(self, connection):
        """Create a new instance of the channel class by using the current
        connection.

        :param ConnectionHandler connection: The given connection to allow
        communication with RabbitMQ.

        """
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
        LOGGER.info('The channel will close in a few time')
        self._channel.close()

    def send_message(self, exchange, queue, message):
        queue_handler = QueueHandler(self._channel, exchange)
        basic_properties = queue_handler.setup_properties()
        # Setup the queue in RabbitMQ before working on it
        queue_handler.setup_queue(queue)

        # Now send the message
        self._channel.basic_publish(exchange=exchange,
                                    routing_key=queue,
                                    body=json.dumps(message),
                                    properties=basic_properties)

    def get_channel(self):
        """Get the current opened connection """
        LOGGER.info('Getting the channel object')
        if self._channel is None:
            raise ChannelDoesntExist('The channel doesn''t exist yet')
        return self._channel

    def consume_message_on_queue(self, queue):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        LOGGER.info('Consuming message on queue : %s', queue)
        self.add_on_cancel_callback()

        try:
            """The queue can be non exist on rabbit, so ChannelClosed exception
            is handled by RabbitMQ and then the TCP connection is closed.
            Re-implement this if others worker can be launch and handle the
            Exception.
            """
            # Get a basic single message
            basic_deliver, properties, body = self._channel.basic_get(queue)
            if basic_deliver is None or basic_deliver.NAME == 'Basic.GetEmpty':
                # Nothing to do when no message
                pass
            else:
                self.on_message(basic_deliver, properties, body)

        except Exception as e:
            LOGGER.error('The Channel was closed. Please open the connection')
            return

    def on_message(self, basic_deliver, properties, body):
        # def on_message(self, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        # LOGGER.info('Received message # %s from %s: %s',
        #            basic_deliver.delivery_tag, properties.app_id, body)
        LOGGER.info('Received message # %s #', body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        LOGGER.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()
