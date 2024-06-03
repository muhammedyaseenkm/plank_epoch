import pika
import json
import time
from tasks import process_task


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()


# Declare a queue
channel.queue_declare(queue='task_queue', durable=True)

# Send messages
for i in range(10):
    message = {'task_id': i, 'data': f'Task {i}'}
    
    # Send tasks to Celery
    await process_task.delay(i)

    # Publish message to RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print(f" [x] Sent {message}")
    time.sleep(1)

process_task.delay(i)

# Close connection
connection.close()
