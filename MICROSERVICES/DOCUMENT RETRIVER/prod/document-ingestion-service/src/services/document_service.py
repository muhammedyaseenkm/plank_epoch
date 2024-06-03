from typing import List, Optional
from models.document import Document, DocumentCreate, DocumentUpdate
from redis import Redis 
import json

class DocumentService:
    def __init__(self, redis_client:Redis):
        self.documents: List[Document] = []
        self.next_id = 1
        self.redis_client = redis_client
        
    async def create_document(self, document_create: DocumentCreate) -> int:
        document = Document(id=self.next_id, name=document_create.name, file_path=document_create.file_path)
        self.documents.append(document)
        self.next_id += 1
        # Store document in Redis
        self.redis_client.set(f"document:{document.id}", json.dumps(document.dict()))
        return document.id
    
    async def get_documnet(self, document_id: int) -> Optional[Document]:
        # Check if document is in Redis
        if self.redis_client:
            document_data = self.redis_client.get(f"document:{document_id}")
            if document_data :
                document_dict = json.loads(document_data)
                return  Document(**document_dict)
        else:
            raise RuntimeError("Cannot fetch connection with Redis")
        
        # Document not found in Redis, fetch from database
        for document in self.documents:
            if document_id == document.id:
                return document
        return None
    
    async def get_all_documents(self) -> List[Document]:
        # In a real application, this method would fetch documents from a database
        return self.documents
    
    async def update_document(self, document_id: int, document_update: DocumentUpdate) -> bool:
        for document in self.documents:
            if document_id == document.id:
                # Update document attributes
                if document_update.name:
                    document.name == document_update.name
                if document_update.file_path:
                    document.file_path == document_update.file_path
                if document_update.processed_at:
                    document.processed_at = document_update.processed_at
                if document_update.is_processed is not None:
                    document.is_processed = document_update.is_processed
                # Update document in Redis
                self.redis_client.set(f"document:{document.id}", json.dumps(document.dict()))
                return True
        return False
    
    async def delete_documnet(self, document_id: int) -> bool:
        for i , document in enumerate(self.documents):
            if document.id == document_id:
                del self.documents[i]
                if self.redis_client:
                    self.redis_client.delete(f"document:{document_id}")
                return True
        return False





