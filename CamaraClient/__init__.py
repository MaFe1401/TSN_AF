import json
import pika
from rabbitmq_queues import *
import os
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)
if __name__ == "__main__":

    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()

    channel.queue_declare(queue='south-cam', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='south-cam', on_message_callback=receive_message)

    print("Waiting to consume")
    channel.start_consuming()