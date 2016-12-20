#!/usr/bin/env python
import sys
sys.path.append('../')
from custum import display_digit


def callback(ch, method, properties, body):
    print(" [x] Received Data : %r" % body)
    process_time = body.count('.')
    print('Time to process this task is %r seconds' % process_time)
    return display_digit(process_time)
