from celery import Celery
sys.path.append('../')
from custum import display_digit

app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task
def my_worker(body='1 second .'):
	print(" [x] Received %r" % body)

	process_time = body.count('.')
	print('Time to process this task is : %r seconds' % process_time)

	ret = display_digit(process_time)

    return ret
