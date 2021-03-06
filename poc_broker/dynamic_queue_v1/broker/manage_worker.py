from threading import Thread, RLock
import time
from broker.rabbit_api import get_all_queue
from broker.worker import Worker


# This process will allow the thread to lock the program until processing
lock = RLock()


class ManageWorker(Thread):

    """
    This thread is in charge to manage the worker when the queue is created.
    It will launch a new worker on each available queue on rabbitmq.
    """

    def __init__(self, host='localhost', port=15672, user_id='guest',
                 password='guest'):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.user_id = user_id
        self.password = password

    def run(self):
        print('... Start the consumer ...')
        process_time = 2  # 2 secondes
        while True:
            # Get all existing queues and check if the queue args exists
            queues = get_all_queue(self.host, self.port,
                                   self.user_id, self.password)
            print('Number of queue : %s' % len(queues))
            for queue in queues:
                # Init a new worker to job on the queue
                worker = Worker()
                # Make a lock until the worker to do all the job about the msg
                with lock:
                    worker.start_consuming(queue)
                time.sleep(process_time)
