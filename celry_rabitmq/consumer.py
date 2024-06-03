import pika
import json
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(" [x] Received %r" % message)
    # Simulate processing
    time.sleep(2)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Assign callback function to consume messages from queue
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
