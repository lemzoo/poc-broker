# !/usr/bin/env python
import time
import json


def callback(channel, method, properties, body):
    decoded_msg = body.decode()
    msg_context = json.loads(decoded_msg)
    print(" [x] Traitement du dossier de ... {0} {1} ..."
          .format(msg_context['nom'], msg_context['prenom']))
    time.sleep(5)
    # import pdb; pdb.set_trace()
    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
    # channel.connection.close()

    return 0


def processor(body):
    decoded_msg = body.decode()
    msg_context = json.loads(decoded_msg)
    print(" [x] Traitement du dossier de ... {0} {1} ..."
          .format(msg_context['nom'], msg_context['prenom']))
    time.sleep(5)
