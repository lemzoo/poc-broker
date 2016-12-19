#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
queue_name = 'rpc_queue'

channel.queue_declare(queue=queue_name)
channel.basic_qos(prefetch_count=1)

result = channel.queue_declare(exclusive=True)
callback_queue = result.method.queue
