# !/usr/bin/env python
from producer import Producer
import time

publisher = Producer()

# Send a message
for i in range(100):
    message = 'Hello World : %s' % i
    publisher.publish(message)
    time.sleep(1)
