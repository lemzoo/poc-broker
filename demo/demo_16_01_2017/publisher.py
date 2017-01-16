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
        "nom": "Polony",
        "prenom": "Christiant"
        },
        {
        "id": "60000",
        "nom": "Sartre",
        "prenom": "Jean-Paul"
        },
        {
        "id": "90000",
        "nom": "Camus",
        "prenom": "Albert"
        }]

if __name__ == '__main__':
    publisher = Producer()

    for message in data:
        print(message)
        queue = 'dossier_{0}_{1}' .format(message['nom'], message['prenom'])
        publisher.publish(queue, message)
        time.sleep(0.1)
