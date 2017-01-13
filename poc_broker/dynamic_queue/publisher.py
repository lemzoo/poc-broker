from pika_client import *
from ticker_system import *


publisher = PikaPublisher(exchange_name="my_exchange")

ticker = Ticker(publisher, "")
ticker.monitor()
