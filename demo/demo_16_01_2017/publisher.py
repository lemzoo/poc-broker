# !/usr/bin/env python
from broker.producer import Producer
import time
import json

if __name__ == '__main__':
    publisher = Producer()

    # Get data from JSON database
    with open('data.json') as data_file:
        data = json.load(data_file)

    for message in data:
        print(message)
        queue = 'dossier_%s_%s' % message["nom"], message["prenom"]
        publisher.publish(queue, message)
        time.sleep(0.1)
