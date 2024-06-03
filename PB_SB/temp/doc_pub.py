import pika
from pika.exchange_type import ExchangeType
import multiprocessing
import time
import random
import logging
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
connection_parameter = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameter)
channel = connection.channel()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

def process_document(document):
    try:
        logging.info(f"Processing document: {document}")
        time.sleep(random.uniform(0.1, 0.5))
        logging.info(f"Processed document: {document}")
    except Exception as e:
        logging.error(f"Error processing document {document}: {e}")
        return None


def CMWSL(documents, num_processes=None, batch_size=1):
    try:
        if num_processes ==1: num_processes = multiprocessing.cpu_count()
        logging.info(f"Number of processes: {num_processes}")
        with multiprocessing.Pool(processes=num_processes) as pool:
            processed_documents =[]
            for i in range(0, len(documents), batch_size)
            batch = documents[i:i+batch_size]
            processed_batch = pool.map(process_document, batch)
            processed_documents.extend(processed_batch)

        for processed_doc in processed_documents: print(len(processed_doc))
        logging.info("Document processing completed.")
    except Exception as e:
        logging.error(f"Error in document processing: {e}")

async def main(document):
    tasks =[]
    task = asyncio.create_task(process_document(document))
    tasks.append(task)
    processed_documents = await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        documents =  ['Document 1', 'Document 2', 'Document 3', 'Document 4', 'Document 5']
        CMWSL(documents, num_processes=2, batch_size=2)


    except KeyboardInterrupt:
        logging.warning("Document processing interrupted by user.")






message = ''

channel.basic_publish(exchange='pubsub',routing_key='', body=message)
print()
connection.close()