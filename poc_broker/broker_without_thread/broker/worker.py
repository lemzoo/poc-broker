# !/usr/bin/env python
import pika
from broker.processor import processor


class Worker():
    def __init__(self, host='localhost', port=5672, user_id='guest',
                 password='guest'):
        self.host = host
        self.port = port
        self.user_id = user_id
        self.password = password
        self.init_app(self.host, self.port, self.user_id, self.password)

    def init_app(self, host, port, user_id, password):
        self.parameters = pika.ConnectionParameters(
            host, port, credentials=pika.PlainCredentials(user_id, password))
        self.connection = pika.BlockingConnection(self.parameters)
        self.open_connection()

    def open_connection(self):
        self.channel = self.connection.channel()

    def close_connection(self):
        self.connection.close()

    def setup_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True,
                                   passive=True, auto_delete=True)

    def stop_consuming(self):
        self.channel.stop_consuming()

    def start_consuming(self, queue_name):

        # Setup the channel before starting consuming
        self.setup_queue(queue_name)

        # Get a basic single message
        method, header, body = self.channel.basic_get(queue=queue_name)

        if method.NAME == 'Basic.GetEmpty':
            self.close_connection()
            return ''
        else:
            processor(body)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            self.close_connection()
