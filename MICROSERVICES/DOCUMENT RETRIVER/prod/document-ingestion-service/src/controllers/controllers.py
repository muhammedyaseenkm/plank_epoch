from fastapi import APIRouter,File, UploadFile, HTTPException, Depends
from typing import List
from models.document import Document, DocumentCreate, DocumentUpdate
from services.document_service import DocumentService
from utils.file_utils import save_document_to_file_system

router = APIRouter()
document_service = DocumentService()

@router.post("/upload", response_model=int)
async def upload_document(
    file: UploadFile = File(...)
    redis_client: Redis = Depends(get_redis_client)
    ):
    file_path = await save_document_to_file_system(file)
    # Process the document (e.g., extract text, analyze content)
    # You can call functions from the services module here

    # Save document metadata to the database
    document_id  = await document_service.create.createDocument(file.filename, file_path)
