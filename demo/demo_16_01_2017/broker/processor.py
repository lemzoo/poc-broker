# !/usr/bin/env python
import time
import json


def callback(channel, method, properties, body):
    received_msg = json.loads(body)
    print(" [x] Received %r" % received_msg)
    time.sleep(1)
    channel.stop_consuming()
