import aiormq
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_document(document):
    try:
        logging.info(f"Processing document: {document}")
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Use asyncio.sleep for non-blocking delay
        logging.info(f"Processed document: {document}")
        return document
    except Exception as e:
        logging.error(f"Error processing document {document}: {e}")
        return None

async def consume_callback(message):
    async with message.process():
        document = message.body.decode()
        processed_doc = await process_document(document)
        if processed_doc: print(processed_doc)
        else :print(f' document {document}  not proceseed')

async def consume():
    try:
        connection = await aiormq.connect("amqp://guest:guest@localhost/")
        channel = await connection.channel()
        
        # Declare the exchange with a fanout type
        await channel.exchange_declare('pubsub', exchange_type='fanout')

        # Declare the queue
        queue_response = await channel.queue_declare(exclusive=True)
        queue_name = queue_response.queue

        # Bind the queue to the exchange
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
    try:
        asyncio.run(consume())
    except KeyboardInterrupt:
        logging.warning("Document processing interrupted by user.")
