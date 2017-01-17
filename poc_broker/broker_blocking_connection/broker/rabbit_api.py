import requests


def get_all_queue(host='localhost', port=15672,
                  user_id='guest', password='guest'):
        url = 'http://%s:%s/api/queues/' % (host, port)
        response = requests.get(url, auth=(user_id, password))
        queues = [q['name'] for q in response.json()]
        return queues
