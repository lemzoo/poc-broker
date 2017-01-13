# !/usr/bin/env python
import time


def callback(channel, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(1)
    channel.stop_consuming()
