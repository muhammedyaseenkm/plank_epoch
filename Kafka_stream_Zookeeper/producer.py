from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'kafka:9092'  # Note the change to 'kafka:9092'
}

producer = Producer(**conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

topic = 'test_topic'

producer.produce(topic, key='key', value='Hello, Kafka!', callback=delivery_report)
producer.flush()
