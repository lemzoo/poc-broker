from broker.producer import Producer
import logging
import time

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ManagePublisher():

    """
    This thread is in charge to manage the worker when the queue is created.
    It will launch a new worker on each available queue on rabbitmq.
    """

    def __init__(self):
        LOGGER.info('Manage Publisher was configured')
        pass

    def send_message(self, queue_name, message):
        LOGGER.info('Sending message on the manager publisher')
        time.sleep(1)
        producer = Producer(queue_name, message)
        producer.run()
