# !/usr/bin/env python
import logging
from broker.rabbit_api import list_queues
from broker.worker import Worker


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
DEFAULT_EXCHANGE = 'SIAEF'


class Consumer(object):
    """This is a  consumer that will manage the worker and the queue. It will
    open the connection one time and then send request to RabbitMQ to get all
    the existing queues. And then after, it will launch a single worker to work
    on a queue above the gotten queue list.

    """

    def __init__(self, connection_handler):
        """
        Instantiate a simple consumer by giving a connection handler which is
        opened and ready to use.

        :param ConnectionHandler connection_handler : The connection between
        the consumer and RabbitMQ.
        """
        self._connection_handler = connection_handler

    def start_working(self):
        LOGGER.info('... Demarage du broker de message ...')
        process_time = 2  # 2 secondes
        while True:
            # Get all existing queues and check if the queue args exists
            queues = list_queues()

            number_queues = len(queues)
            LOGGER.info('Nombre de dossier a traiter : %s', number_queues)
            for queue in queues:
                # Init a new worker to job on the queue
                worker = Worker(self._connection_handler, queue)

                # Make a lock until the worker to do all the job about the msg
                worker.consume_message()
                self._connection_handler.sleep(1)
            if number_queues == 0:
                process_time += 0.5
            LOGGER.info('No queue. Consumer is waiting for %s s', process_time)
            self._connection_handler.sleep(process_time)
