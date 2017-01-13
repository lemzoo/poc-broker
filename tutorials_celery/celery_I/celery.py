#!/usr/bin/env python

from __future__ import absolute_import
from celery import Celery

app = Celery('celery_I',
             broker='amqp://jimmy:jimmy123@localhost/jimmy_vhost',
             backend='rpc://',
             include=['celery_I.tasks'])


CELERY_QUEUES = {
    "default": {
        "exchange": "default",
        "binding_key": "default"},
    "longtime": {
        "exchange": "media",
        "exchange_type": "topic",
        "binding_key": "media.video",
    },
    "process": {
        "exchange": "media",
        "exchange_type": "topic",
        "binding_key": "media.image",
    }
}
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"

"""
CELERY_ROUTES = (
    {
        "celery_I.tasks.longtime_add": {
            "queue": "longtime",
            "routing_key": "longtime.add"
        }
    },
)
"""
CELERY_ROUTES = {"feed.tasks.import_feed": {"queue": "feeds"}}
