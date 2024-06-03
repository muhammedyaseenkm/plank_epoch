from fastapi import FastAPI,File,UploadFile
import os 
import shutil
import logging

app =FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Data Storage Server')

UPLOAD_FOLDER = "data_storage"
@app.post('/upload/')
async def upload_file(file:UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_FOLDER,exist_ok=True)
        file_path  = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File uploaded: {file_path}")
        return {"message": "File uploaded successfully", "file_path": file_path}
    
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {e}")
        return {"erro":str(e)}
    
@app.post('/store/')
async def store_data(file_path:str):
    try:
        # Move file to storage location
        new_file_path = os.path.join(UPLOAD_FOLDER,os.path.basename(file_path))
        shutil.move(file_path, new_file_path)
        logger.info(f"Data stored: {new_file_path}")
        return {"message": "Data stored successfully", "file_path": new_file_path}      
      
    except Exception as e:
        logger.error(f"Error occurred while storing data: {e}")
        return {"error": str(e)}
