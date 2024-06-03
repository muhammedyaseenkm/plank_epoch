from fastapi import FastAPI, UploadFile, File
import shutil
import os
from pdfplumber import open as open_pdf

app = FastAPI()

UPLOAD_FOLDER = "uploads"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF file and extract text
        with open_pdf(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        
        return {"message": "File uploaded successfully", "file_path": file_path, "text": text}
    except Exception as e:
        return {"error": str(e)}
