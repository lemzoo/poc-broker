#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue_name = 'task_queue'
channel.queue_declare(queue=queue_name, durable=True)
