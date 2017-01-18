from broker.producer import Producer
from broker.producer import logging, LOG_FORMAT


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
    example = Producer('amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600')
    example.run()


if __name__ == '__main__':
    main()
