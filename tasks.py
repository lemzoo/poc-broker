from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y, max):
    ret = 0
    for i in range(max):
        ret += x + y
    return ret
