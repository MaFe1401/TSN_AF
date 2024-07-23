import pika
import time
import os
from APICallFunctions import *
def receive_message(ch, method, properties, body):

    print('received msg : ', body.decode('utf-8'))
    time.sleep(2)
    print('acking it')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    qosFlows = QoSmapping(body.decode('utf-8'))
    print("----QOS PROFILES----")
    print(qosFlows)
    for qosProfile in qosFlows:
        createSession(qosProfile)
