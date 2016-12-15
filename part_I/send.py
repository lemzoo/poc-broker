#!/usr/bin/env python
from setup import connection, channel

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
print("The connection is closed")
