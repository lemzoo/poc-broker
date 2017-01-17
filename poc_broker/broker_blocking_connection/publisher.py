# !/usr/bin/env python
from broker.producer import Producer
import time


data = [{
        "id": "00001",
        "nom": "Dupont",
        "prenom": "Jean"
        },

        {
        "id": "10000",
        "nom": "Blanc",
        "prenom": "Louis"
        },

        {
        "id": "20000",
        "nom": "Karhamazov",
        "prenom": "Dimitry"
        },

        {
        "id": "30000",
        "nom": "Sorel",
        "prenom": "Julien"
        },

        {
        "id": "40000",
        "nom": "Valjean",
        "prenom": "Jean"
        },

        {
        "id": "50000",
        "nom": "Vian",
        "prenom": "Boris"
        },

        {
        "id": "60000",
        "nom": "Javert",
        "prenom": "Jean"
        },

        {
        "id": "70000",
        "nom": "Martin",
        "prenom": "Paul"
        },

        {
        "id": "90000",
        "nom": "Camus",
        "prenom": "Albert"
        }
        ]

if __name__ == '__main__':
    publisher = Producer()

    for i in range(10):
        for message in data:
            queue = 'dossier_{0}_{1}' .format(message['nom'], message['prenom'])
            publisher.publish(queue, message)
            time.sleep(0.001)
