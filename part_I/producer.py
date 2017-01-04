#!/usr/bin/env python
from setup import connection, channel, queue_name

message = 'Hello World!'

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=message)

print(" [x] Sent 'Hello World!'")

connection.close()
print("The connection is closed")
