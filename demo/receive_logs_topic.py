#!/usr/bin/env python
import sys
sys.path.append('../')
from custum import display_digit


def worker(ch, method, properties, body):
    print(" [x] Received Data : %r:%r" % (method.routing_key, body))

    process_time = body.count(b'.')
    print('Time to process this task is %r seconds' % process_time)
    display_digit(process_time)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
