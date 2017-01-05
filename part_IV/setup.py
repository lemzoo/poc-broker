#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

exchange_name = 'direct_logs'
exchange_type = 'direct'
channel.exchange_declare(exchange=exchange_name, type=exchange_type)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange=exchange_name,
                       queue=queue_name,
                       routing_key=severity)
