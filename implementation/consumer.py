from broker.worker import Worker
from broker.worker import logging, LOG_FORMAT


def main() :
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    example = Worker('amqp://guest:guest@localhost:5672/%2F')
    try:
        example.run()
    except KeyboardInterrupt:
        example.stop()


if __name__ == '__main__':
    main()
