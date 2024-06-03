from fastapi import FastAPI, File, UploadFile
import requests
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Display Server")

STORAGE_SERVER_URL = "http://localhost:8000/upload/"
PROCESS_SERVER_URL = "http://localhost:8001/process/"

@app.post("/upload/")
async def upload_file(file:UploadFile=File(...)):
    try:
        response = requests.post(STORAGE_SERVER_URL, files={"file": (file.filename, file.file)})
        data = response.json()
        logger.info(f"File uploaded to storage server: {data['file_path']}")
        return data
    
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {e}")
        return {"error": str(e)}


@app.post('/process/')
async def share_data(file_path:str):
    try:
        response = requests.post(STORAGE_SERVER_URL, json={"file_path": file_path})
        data = response.json()
        logger.info(f"Data shared with storage server: {data['file_path']}")
        return data
    
    except Exception as e:
        logger.error(f"Error occurred while sharing data: {e}")
        return {"error": str(e)}
    print('hai')
    



    
