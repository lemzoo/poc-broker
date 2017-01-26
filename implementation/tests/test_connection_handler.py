import unittest
import sys
import pika

sys.path.append('/vagrant/code/poc-broker/implementation/broker')
from broker.connection_handler import ConnectionHandler


class TestConnnectionHandler(unittest.TestCase):

    def test_init_app(self):
        connection_handler = ConnectionHandler()
        self.assertIs(True,connection_handler._connection.is_open)
        self.assertIsInstance(connection_handler._connection, pika.BlockingConnection)
        self.assertIsNotNone(connection_handler._connection)

    def test_get_connection(self):
        connection_handler = ConnectionHandler()
        self.assertIs(True, connection_handler._connection.is_open)
        self.assertIsNotNone(connection_handler._connection)

    def test_close_connection(self):
        connection_handler = ConnectionHandler()
        connection_handler.close_connection()
        self.assertIs(True,connection_handler._connection.is_closed)
