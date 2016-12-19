#!/usr/bin/env python
import sys
from setup import connection, channel, exchange_name
import pika


severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

message = ' '.join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(exchange=exchange_name,
                      routing_key=severity,
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2, ))
# 2 is meaning the message is persistent
print(" [x] Sent %r:%r" % (severity, message))

connection.close()
