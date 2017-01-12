# !/usr/bin/env python
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
