# !/usr/bin/env python
import pika
from broker.rabbit_api import get_all_queue
import json


class Producer():
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
        print("The connection is closed ...")

    def setup_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True,
                                   auto_delete=True)

    def publish(self, queue='hello', message={'Hello World !'}):
        # Get all existing queues and check if the queue args exists
        queues = get_all_queue(self.host, 15672,
                               self.user_id, self.password)
        if queue not in queues:
            self.setup_queue(queue)

        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=json.dumps(message))
        print("=> Evenement sur dossier :", message["nom"], message["prenom"])
