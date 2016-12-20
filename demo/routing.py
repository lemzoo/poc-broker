#!/usr/bin/env python
from setup import channel, queue_name
from receive_logs_topic import worker

channel.basic_consume(worker, queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
