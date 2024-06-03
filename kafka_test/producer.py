from confluent_kafka import Producer

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'

# Create Producer instance
producer = Producer({'bootstrap.servers': bootstrap_servers})

# Topic to produce messages to
topic = 'test_topic'

# Produce a message
message = "Hello, Kafka!"
producer.produce(topic, message.encode('utf-8'))

import time
while True:
    # Flush the producer
    producer.flush()
    time.sleep(10)    
    print("Message sent successfully!")
