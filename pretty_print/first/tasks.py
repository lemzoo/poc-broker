from celery import Celery

app = Celery('tasks', broker='amqp://localhost//', backend='mysql://root:root@localhost/celery_db')


@app.task
def reverse(string):
    return string[::-1]
