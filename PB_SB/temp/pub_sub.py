import pika
from pika.exchange_type import ExchangeType

# Connection parameters
connection_parameters = pika.ConnectionParameters('localhost')

# Establishing connection
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Declaring fanout exchange
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# Publishing message to the exchange
message = "HELLO MESSAGE"
channel.basic_publish(exchange='pubsub', routing_key="", body=message)
print(f'Sent Message: {message}')

# Closing the connection
connection.close()

# Setting up message receiver function
def on_message_received(ch, method, properties, body):
    print(f"Received message: {body}")

# Establishing another connection
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
