#!/usr/bin/env python
import sys
from setup import connection, channel, queue_name
import pika

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2, ))
# 2 is meaning the message is persistent
print(" [x] Sent %r" % message)

connection.close()
