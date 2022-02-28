#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import pika
import backoff
from typing import Callable

def backoff_connect(details):
    print ("Backing off connecting to AMQP for {wait:0.1f} seconds afters {tries} tries".format(**details))

def backoff_reconnect(details):
    print ("Backing off reconnecting to AMQP for {wait:0.1f} seconds afters {tries} tries".format(**details))

class AMQPConsumer(object):
    def __init__(self,host: str = None,queue: str = None,username: str = None,password: str = None,port: int = None,callback = None,vhost: str = '%2f'):
        self.host = host
        self.queue = queue
        self.username = username
        self.password = password
        self.port = port
        self.vhost = vhost
        self.callback = callback
        self.url = f"amqp://{username}:{password}@{host}:{port}/{vhost}"

    @backoff.on_exception(backoff.fibo, pika.exceptions.AMQPConnectionError, max_tries=20, on_backoff=backoff_connect)
    def amqp_connect(self):
        parameters = pika.URLParameters(self.url)
        return pika.BlockingConnection(parameters)

    @backoff.on_exception(backoff.constant, (pika.exceptions.ConnectionClosed,pika.exceptions.AMQPChannelError), max_tries=15, on_backoff=backoff_reconnect)
    def connect_consume(self):
        self.connection = self.amqp_connect()
        print("connected to amqp")
        self.channel = self.connection.channel()
        self.channel.basic_consume(self.queue,self.callback)
        self.channel.start_consuming()
