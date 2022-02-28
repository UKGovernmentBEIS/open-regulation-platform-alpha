#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

from amqp_consumer import AMQPConsumer
import argparse

def email(ch,method,properties,body):
    print("received %r" % body)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #ch.basic_nack(delivery_tag = method.delivery_tag, requeue=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="consume from amqp queue")
    parser.add_argument('-H','--host',required=True)
    parser.add_argument('-v','--vhost',default="%2f") # uri encoded /
    parser.add_argument('-q','--queue',required=True)
    parser.add_argument('-u','--username',required=True)
    parser.add_argument('-p','--password',required=True)
    parser.add_argument('-P','--port',default=5672,type=int)
    args = parser.parse_args()

    consumer = AMQPConsumer(**vars(args),callback=email)

    consumer.connect_consume()
