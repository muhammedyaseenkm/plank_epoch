from fastapi import FastAPI, BackgroundTasks
import logging
import time
import requests

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Processor Server")

STORAGE_SERVER_URL = "http://localhost:8000/store/"

@app.post("/process/")
async def process_data(background_tasks: BackgroundTasks, file_path: str):
    background_tasks.add_task(process_data_task, file_path)
    return {"message": "Data processing initiated"}

def process_data_task(file_path:str):
    # Perform data processing here
    logger.info(f"Data processing initiated for file: {file_path}")
    time.sleep(5)
    logger.info(f"Data processing completed for file: {file_path}")

    # Inform storage server to store the processed data
    try:
        response = requests.post(STORAGE_SERVER_URL, json={'file_path':file_path})
        data = response.json()
        logger.info(f"Processed data stored: {data['file_path']}")

    except Exception as e:
        logger.error(f"Error occurred while storing processed data: {e}")







