from broker.manage_publisher import ManagePublisher
from messages import data
from broker.producer import logging, LOG_FORMAT
import time


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    publisher = ManagePublisher()
    time.sleep(2)
    for i in range(10):
        for message in data:
            queue_name = message['id']
            publisher.send_message(queue_name, message)


if __name__ == '__main__':
    main()
