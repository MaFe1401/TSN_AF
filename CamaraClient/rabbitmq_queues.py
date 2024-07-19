import pika
import time
import os

def receive_message(ch, method, properties, body):

    print('received msg : ', body.decode('utf-8'))
    time.sleep(2)
    print('acking it')
    ch.basic_ack(delivery_tag=method.delivery_tag)

    