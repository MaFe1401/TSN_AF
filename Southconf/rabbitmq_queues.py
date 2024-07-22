import pika
import os
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

def send_message(message, queue_name):
    print("URL: "+amqp_url)
    print("TRYING TO ESTABLISH CONNECTION")
    connection = pika.BlockingConnection(url_params)
    print("CONNECTION STABLISHED")
    channel = connection.channel()
    print("CHANNEL CREATED")
    channel.queue_declare(queue=queue_name, durable=True)
    print("QUEUE DECLARED")
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print("MESSAGE PUBLISHED")
    print("Message sent to RabbitMQ")
    connection.close()