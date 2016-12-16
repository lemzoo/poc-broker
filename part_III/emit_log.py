#!/usr/bin/env python
import sys
from setup import connection, channel
import pika

message = ' '.join(sys.argv[1:]) or "info : Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2, ))
# 2 is meaning the message is persistent
print(" [x] Sent %r" % message)

connection.close()
