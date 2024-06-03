import os
import time
import requests
from kafka import KafkaProducer
import json
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
STOCK_API_URL = 'https://www.alphavantage.co/query'
STOCK_API_KEY = 'your_api_key'  # Replace with your actual API key
SYMBOL = 'AAPL'
INTERVAL = '1min'
TOPIC_NAME = 'stock-data'

def fetch_stock_data(symbol, interval, api_key):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': api_key
    }
    response = requests.get(STOCK_API_URL, params=params)
    data = response.json()
    return data

def create_kafka_producer(broker):
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=broker,
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            return producer
        except NoBrokersAvailable:
            print("No brokers available, retrying in 5 seconds...")
            time.sleep(5)

def main():
    producer = create_kafka_producer(KAFKA_BROKER)
    while True:
        stock_data = fetch_stock_data(SYMBOL, INTERVAL, STOCK_API_KEY)
        if "Time Series" in stock_data:
            for timestamp, values in stock_data["Time Series (1min)"].items():
                data = {'timestamp': timestamp, 'values': values}
                producer.send(TOPIC_NAME, value=data)
                print(f"Sent data to Kafka: {data}")
        time.sleep(60)  # Fetch data every minute

if __name__ == '__main__':
    main()
