from broker.manage_publisher import ManagePublisher
from broker.connection_handler import ConnectionHandler
from broker.channel_handler import ChannelHandler
from broker.exchange_handler import ExchangeHandler

from messages import data
from broker.producer import logging, LOG_FORMAT
import time


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    AMQP_URL = 'amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600'
    # Create a connection handler
    connection_handler = ConnectionHandler(AMQP_URL)
    # Open connection
    connection = connection_handler.open_and_get_connection()
    print('is connection opened : ', connection.is_open)
    print('is connection closed : ', connection.is_closed)
    import pdb; pdb.set_trace()
    connection.connect()
    print('is connection opened : ', connection.is_open)
    print('is connection closed : ', connection.is_closed)

    # Create a channel handler
    channel_handler = ChannelHandler()
    # Create new channel
    channel = channel_handler.create_new_channel(connection)
    print('channel is created : ', channel)
    import pdb; pdb.set_trace()
    # Create Exchange one time
    exchange_handler = ExchangeHandler()
    exchange_name = exchange_handler.create_exchange(channel_handler, 'SIAEF')
    print('Exchange is created with this name : ', exchange_name)

    # Close the channel
    channel_handler.close_channel()
    # Close connection
    connection_handler.close_connection()

    publisher = ManagePublisher()

    time.sleep(2)
    """
    for i in range(10):
        for message in data:
            queue_name = message['id']
            publisher.send_message(queue_name, message)
    """


if __name__ == '__main__':
    main()
