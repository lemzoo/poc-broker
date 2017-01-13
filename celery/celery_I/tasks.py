#!/usr/bin/env python

from __future__ import absolute_import
from test_celery.celery import app
import time

import sys
sys.path.append('../../')
from custum import display_digit


@app.task
def longtime_add(x, y):
    print('long time task begins')
    # sleep 5 seconds
    time.sleep(5)
    print('long time task finished')
    return x + y


@app.task
def process_tasks(body='Hello World !.'):
    print(" [x] Received Data : %r" % body)
    process_time = body.count('.')
    print('Time to process this task is %r seconds' % process_time)
    ret = display_digit(process_time)
    return ret
