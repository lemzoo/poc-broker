#!/usr/bin/env python
import sys
from setup import connection, channel, exchange_name
import pika

message = ' '.join(sys.argv[1:]) or "info : Hello World!"
channel.basic_publish(exchange=exchange_name,
                      routing_key='',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2, ))
print(" [x] Sent %r" % message)

connection.close()
