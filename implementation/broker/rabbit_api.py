import requests
from pyrabbit.api import Client


def get_all_queue(host='localhost', port=15672,
                  user_id='guest', password='guest'):
        url = 'http://%s:%s/api/queues/' % (host, port)
        response = requests.get(url, auth=(user_id, password))
        queues = [q['name'] for q in response.json()]
        return queues


def list_queues(host='localhost', port=15672,
                user_id='guest', password='guest'):
    url = '%s:%s' % (host, port)
    client = Client(url, user_id, password)
    queues = [q['name'] for q in client.get_queues()]
    return queues
