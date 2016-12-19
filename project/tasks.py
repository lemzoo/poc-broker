from celery import Celery
import time


app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')

def display_digit(number):
	for i in range(0, number):
		char = '.'
		print(char, sep='', end='', flush=True)
		time.sleep(1)

	print(" [x] Done")
	return number


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
	
	return display_digit(process_time)
