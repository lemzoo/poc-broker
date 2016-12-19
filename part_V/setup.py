#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

exchange_name = 'topic_logs'
exchange_type = 'topic'
channel.exchange_declare(exchange=exchange_name, type=exchange_type)
channel.basic_qos(prefetch_count=1)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_keys]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange=exchange_name,
                       queue=queue_name,
                       routing_key=binding_key)
