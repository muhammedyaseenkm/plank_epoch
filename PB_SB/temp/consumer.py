import pika

# Setting up message receiver function
def on_message_received(ch, method, properties, body):
    print(f"Received message: {body}")

# Connection parameters
connection_parameters = pika.ConnectionParameters('localhost')

# Establishing connection
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Declaring a queue
channel.queue_declare(queue='letterbox')

# Binding the queue to the exchange
channel.queue_bind(exchange='pubsub', queue='letterbox')

# Setting up a consumer
channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_message_received)

print('Start Consuming')
# Start consuming messages
channel.start_consuming()
