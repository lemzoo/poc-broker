#!/usr/bin/env python
from setup import channel, queue_name
from worker import callback

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
