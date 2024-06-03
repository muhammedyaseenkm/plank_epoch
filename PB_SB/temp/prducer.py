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
