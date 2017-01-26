# !/usr/bin/env python
from broker.consumer import Consumer
from broker.connection_handler import ConnectionHandler
from broker.consumer import logging, LOG_FORMAT


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    connection_handler = ConnectionHandler()

    consumer = Consumer(connection_handler)
    consumer.start_working()


if __name__ == '__main__':
    main()
