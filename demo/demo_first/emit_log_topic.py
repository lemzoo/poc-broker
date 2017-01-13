#!/usr/bin/env python
import sys
from setup import connection, channel, exchange_name
import pika


routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

message = ' '.join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(exchange=exchange_name,
                      routing_key=routing_key,
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2, ))
print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()
