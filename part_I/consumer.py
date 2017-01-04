#!/usr/bin/env python
from setup import channel
from receive import callback

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
