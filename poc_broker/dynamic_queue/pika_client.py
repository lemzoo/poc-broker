import pika


class PikaPublisher(object):
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
        self.queue_exists = False

    def publish(self, message, routing_key):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost', credentials=pika.PlainCredentials('guest', 'guest')))
        """
        connection = pika.AsyncoreConnection(
            pika.ConnectionParameters(
                '127.0.0.1',
                credentials=pika.PlainCredentials('guest', 'guest')))
        """
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange_name,
                                 type="fanout",
                                 durable=False,
                                 auto_delete=False)

        channel.basic_publish(exchange=self.exchange_name,
                              routing_key=routing_key,
                              body=message,
                              properties=pika.BasicProperties(
                                  content_type="text/plain",
                                  delivery_mode=2,))

        channel.close()
        connection.close()

    def monitor(self, qname, callback):
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    'localhost',
                    credentials=pika.PlainCredentials('guest', 'guest')))

            channel = connection.channel()

            if not self.queue_exists:
                channel.queue_declare(queue=qname,
                                      durable=False,
                                      exclusive=False,
                                      auto_delete=False)
                channel.queue_bind(queue=qname, exchange=self.exchange_name)
                print("Binding queue %s to exchange %s" %
                      (qname, self.exchange_name))
                # ch.queue_bind(queue=qname,
                #                exchange=self.exchange_name,
                #                routing_key=qname)
                self.queue_exists = True

            channel.basic_consume(callback, queue=qname)
            # channel.start_consuming()
            pika.asyncore()
            print('Close reason : ', connection.connection_close)
