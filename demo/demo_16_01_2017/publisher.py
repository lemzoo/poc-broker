# !/usr/bin/env python
from broker.producer import Producer
import time
import json


if __name__ == '__main__':
    publisher = Producer()

    # Get data from JSON database
    with open('data.json') as data_file:
        data = json.load(data_file)

    for i in data.len:
        print(data[i])
        queue = 'dossier_%s_%s' % data[i]['nom'], data[i]['prenom']
        message = 'Traitement du dossier : %s %s' % data[i]['nom'], data[i]['prenom']
        publisher.publish(queue, message)
        time.sleep(0.1)

    # # Send a message
    # for i in range(10):
    #     queue = 'my_custum_queue_%s' % i
    #     message = 'Hello World : %s' % i
    #     publisher.publish(queue, message)
    #     time.sleep(0.1)
