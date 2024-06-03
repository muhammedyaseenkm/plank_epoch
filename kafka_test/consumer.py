from confluent_kafka import Consumer, KafkaError

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'

# Create Consumer instance
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to topic
topic = 'test_topic'
consumer.subscribe([topic])

# Consume messages
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition, ignore
                continue
            else:
                # Error, stop consuming
                print(msg.error())
                break

        print('Received message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    pass

finally:
    # Clean up consumer
    consumer.close()
