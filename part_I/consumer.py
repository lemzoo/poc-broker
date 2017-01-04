#!/usr/bin/env python
from setup import channel, queue_name

from receive import callback

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
