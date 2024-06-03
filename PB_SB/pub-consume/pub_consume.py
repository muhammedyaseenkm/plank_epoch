import pika
import logging
import aiormq
import asyncio
import random

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

async def process_document(document):
    try:
        logging.info(f"Processing document: {document}")
        await asyncio.sleep(random.uniform(0.1, 0.5))
        logging.info(f"Processed document: {document}")
        return document

    except Exception as e:
        logging.error(f"Error processing document {document}: {e}")
        return None
    
async def consume_callback(message):
    async with message.process():
        document = message.body.decode()
        processed_doc = await process_document(document)
        if processed_doc:
            print(f"Processed document: {processed_doc}")
        else:
            print(f"Document {document} not processed")

async def consume():
    try:
        connection = await aiormq.connect("amqp://guest:guest@localhost/")
        channel = await connection.channel()
        await channel.exchange_declare('pubsub', exchange_type='fanout')
        queue_response = await channel.queue_declare(exclusive=True)
        queue_name = queue_response.queue
        await channel.queue_bind(exchange='pubsub', queue=queue_name)
        await channel.basic_qos(prefetch_count=1)
        await channel.basic_consume(queue_name, consume_callback)

    except aiormq.exceptions.ChannelClosed as e:
        logging.error(f"Channel closed by server: {e}")
    except aiormq.exceptions.ConnectionClosed as e:
        logging.error(f"Connection closed by server: {e}")
    except Exception as e:
        logging.error(f"Error consuming documents: {e}")

if __name__ == "__main__":
    documents = ['Document 1', 'Document 2', 'Document 3', 'Document 4', 'Document 5']
    publish_documents(documents)

    try:
        asyncio.run(consume())
    except KeyboardInterrupt:
        logging.warning("Document processing interrupted by user.")
