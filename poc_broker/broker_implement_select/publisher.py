from broker.manage_publisher import ManagePublisher
from broker.configuration import ConnectionHandler
from messages import data
from broker.producer import logging, LOG_FORMAT
import time


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    import pdb; pdb.set_trace()
    AMQP_URL = 'amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600'
    connection = ConnectionHandler(AMQP_URL)

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
