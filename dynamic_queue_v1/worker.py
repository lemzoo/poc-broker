# !/usr/bin/env python
import pika
from processor import callback


class Worker():
    def __init__(self, host='localhost', port=5672, user_id='guest',
                 password='guest'):
        self.parameters = pika.ConnectionParameters(
            host, port, credentials=pika.PlainCredentials(user_id, password))
        self.connection = pika.BlockingConnection(self.parameters)
        self.open_connection()

    def open_connection(self):
        self.channel = self.connection.channel()
        self.queue_name = 'hello'
        self.channel.queue_declare(queue=self.queue_name)

    def close_connection(self):
        self.connection.close()
        print("The connection is closed")

    def start_consuming(self):
        self.channel.basic_consume(callback,
                                   queue=self.queue_name,
                                   no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
