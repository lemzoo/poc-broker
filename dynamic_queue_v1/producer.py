# !/usr/bin/env python
import pika


class Producer():
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

    def publish(self, message='Hello World !'):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=message)
        print(" [x] Sent %s ", message)
