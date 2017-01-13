from celery import Celery


app = Celery('tasks_a')
# Config from the module celeryconfig.py
# app.config_from_object('celeryconfig')


# Using a configuration class/object¶
class Config:
    enable_utc = True,
    timezone = 'Europe/Paris'


# Config from the object config
app.config_from_object(Config)


@app.task
def add(x, y):
    return x + y


if __name__ == '__main__':
    app.worker_main()
