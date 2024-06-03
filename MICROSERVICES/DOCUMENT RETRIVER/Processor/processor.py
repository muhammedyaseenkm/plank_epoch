from fastapi import FastAPI, File, UploadFile
from typing import List
import os
import shutil
import requests 

app = FastAPI()

# Function to upload file to Server B
def upload_file_to_server_b(file_path):
    url = "http://localhost:8000/upload/"  # Server B's upload endpoint
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    return response.json()

@app.post("/process/")
async def process_and_save(files: List[UploadFile] = File(...)):
    result = []
    saved_files = []
    
    for i, file in enumerate(files):
        folder_name = f"folder_{i+1}" 
        folder_path = os.path.join("uploads", folder_name)
        os.makedirs(folder_path, exist_ok=True)  
        file_path = os.path.join(folder_path, file.filename)      

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_path)

        # Upload file to Server B and get text data
        upload_response = upload_file_to_server_b(file_path)
        result.append({"file": file_path, "text": upload_response.get("text", ""), "upload_response": upload_response})
    
    return {"files_saved": saved_files, "processing_results": result}
