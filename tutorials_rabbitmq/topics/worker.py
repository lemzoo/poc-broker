#!/usr/bin/env python


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)
