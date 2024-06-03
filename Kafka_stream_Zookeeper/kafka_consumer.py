from kafka import KafkaConsumer
import json

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to consume from
topic_name = 'stock-data'

# Create KafkaConsumer instance
consumer = KafkaConsumer(topic_name,
                         group_id='stock-consumer-group',
                         bootstrap_servers=bootstrap_servers,
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Consume messages
for message in consumer:
    print(f"Received message: {message.value}")

# Close consumer
consumer.close()
