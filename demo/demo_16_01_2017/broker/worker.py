# !/usr/bin/env python
import pika
from broker.processor import callback


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
        # print('... Opening the connection to rabbitmq ...')
        self.channel = self.connection.channel()

    def close_connection(self):
        # print("... The connection will be closed in a few second ...")
        self.connection.close()
        # print("... The connection is closed ...")

    def setup_queue(self, queue_name):
        # print('... Setting the queue `%s` ...' % queue_name)
        self.channel.queue_declare(queue=queue_name, durable=True,
                                   auto_delete=True)

    def stop_consuming(self):
        # print('... The worker stopped to consume message ...')
        self.channel.stop_consuming()

    def start_consuming(self, queue_name):

        # Setup the channel before starting consuming
        self.setup_queue(queue_name)
        self.channel.basic_consume(callback,
                                   queue=queue_name)
        print('...  [*] Waiting for messages. To exit press CTRL+C')

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop_consuming()
        self.close_connection()
