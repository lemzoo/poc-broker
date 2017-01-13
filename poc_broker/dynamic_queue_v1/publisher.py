# !/usr/bin/env python
from broker.producer import Producer
import time


if __name__ == '__main__':
    publisher = Producer()

    # Send a message
    for i in range(10):
        queue = 'my_custum_queue_%s' % i
        message = 'Hello World : %s' % i
        publisher.publish(queue, message)
        time.sleep(0.1)
