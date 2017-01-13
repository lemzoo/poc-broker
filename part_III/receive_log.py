#!/usr/bin/env python

import sys
sys.path.append('../')
from custum import display_digit


def callback(ch, method, properties, body):
    print(" [x] Received Data : %r" % body)
    process_time = body.count(b'.')
    print('Time to process this task is %r seconds' % process_time)

    ret = display_digit(process_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return ret
