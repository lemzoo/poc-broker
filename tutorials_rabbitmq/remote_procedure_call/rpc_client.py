#!/usr/bin/env python

import pika
import uuid
from setup import connection, channel, callback_queue


class FibonacciRpcClient(object):
    def __init__(self):

        self.connection = connection
        self.channel = channel
        self.callback_queue = callback_queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties
                                        (
                                            reply_to=self.callback_queue,
                                            correlation_id=self.corr_id,
                                        ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()
number = 50
print(" [x] Requesting fib(%r)" % number)
response = fibonacci_rpc.call(number)
print(" [.] Got %r" % response)
