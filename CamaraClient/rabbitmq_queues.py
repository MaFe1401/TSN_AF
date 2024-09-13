import pika
import time
import os
import json
from APICallFunctions import *

def receive_message(ch, method, properties, body):

    print('received msg : ', json.loads(body))
    time.sleep(2)
    print('acking it')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    qosFlows = QoSmapping(json.loads(body))
    print("----QOS PROFILES----")
    print(qosFlows)
    for qosProfile in qosFlows:
        createSession(qosProfile)
