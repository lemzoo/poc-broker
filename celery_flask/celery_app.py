from flask import Flask
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_BACKEND'] = 'mysql://root:root@localhost/celery_tasks'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/celery_async'


celery = make_celery(app)
db = SQLAlchemy(app)


class Results(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.String(50))


@app.route('/insertData')
def insertData():
    return insert()


@app.route('/process/<name>')
def process(name):
    return reverse.delay(name)


@celery.task
def reverse(string):
    return string[::-1]


def insert():
    for i in range(500):
        data = ''.join(choice('ABCDE') for i in range(10))
        result = Results(data=data)

        db.session.add(result)

    db.session.commit()

    return 'Done !'


if __name__ == '__main__':
    app.run(debug=True)
