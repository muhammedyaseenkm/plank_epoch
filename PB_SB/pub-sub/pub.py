import pika
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def publish_documents(documents):
    try:
        connection_parameter = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connection_parameter)
        channel = connection.channel()
        channel.exchange_declare(exchange='pubsub', exchange_type='fanout')

        for document in documents:
            channel.basic_publish(exchange='pubsub', routing_key='', body=document)
            logging.info(f"Published document: {document}")

        connection.close()
    except Exception as e:
        logging.error(f"Error publishing documents: {e}")

if __name__ == "__main__":
    documents = ['Document 1', 'Document 2', 'Document 3', 'Document 4', 'Document 5']
    publish_documents(documents)
