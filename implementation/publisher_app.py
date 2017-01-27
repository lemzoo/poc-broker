# !/usr/bin/env python
from datetime import datetime
from broker.producer import Producer
from broker.connection_handler import ConnectionHandler
from messages import data
from broker.producer import logging, LOG_FORMAT


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    connection_handler = ConnectionHandler()
    connection = connection_handler.get_connection()
    publisher = Producer(connection)
    for i in range(2):
        for message in data:
            queue = message['id']
            now = datetime.now()
            str_now = now.isoformat()
            message['event_hour'] = str_now
            publisher.publish(queue, message)
            connection.sleep(0.1)


if __name__ == '__main__':
    main()
