import pytest

from pika import BlockingConnection
from pika.exceptions import ConnectionClosed

from broker.connection_handler import ConnectionHandler

class TestConnnectionHandler():

    def test_init_app(self):
        connection_handler = ConnectionHandler()
        assert True == connection_handler._connection.is_open
        assert isinstance(connection_handler._connection, BlockingConnection)
        assert connection_handler._connection is None

    def test_open_connection_with_bad_credential(self):
        with pytest.raises(ConnectionClosed):
             connection_handler =  ConnectionHandler('localhost',5555,'guest','guest')

    def test_get_connection(self):
        connection_handler = ConnectionHandler()
        assert True == connection_handler._connection.is_open
        assert connection_handler._connection is not None

    def test_close_connection(self):
        connection_handler = ConnectionHandler()
        connection_handler.close_connection()
        assert True == connection_handler._connection.is_closed
