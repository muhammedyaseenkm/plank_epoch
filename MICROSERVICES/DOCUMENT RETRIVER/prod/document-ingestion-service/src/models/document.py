# models/document.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    """
    Base schema for document attributes.
    
    Attributes:
        name (str): The name of the document.
        file_path (str): The file path of the document.
        uploaded_at (datetime): The timestamp when the document was uploaded.
        processed_at (datetime, optional): The timestamp when the document was processed.
        is_processed (bool): Indicates whether the document has been processed.
    """
    name: str = Field(..., title="Document Name", description="The name of the document")
    file_path: str = Field(..., title="File Path", description="The file path of the document")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, title="Uploaded At", description="The timestamp when the document was uploaded")
    processed_at: Optional[datetime] = Field(None, title="Processed At", description="The timestamp when the document was processed")
    is_processed: bool = Field(False, title="Is Processed", description="Indicates whether the document has been processed")

class DocumentCreate(BaseModel):
    """
    Schema for creating a new document.
    
    Inherits: DocumentBase: Base schema for document attributes.
    """
    name: str = Field(..., title="Document Name", description="The name of the document")
    file_path: str = Field(..., title="File Path", description="The file path of the document")

class DocumentUpdate(BaseModel):
    """
    Schema for updating an existing document.
    
    Inherits: DocumentBase: Base schema for document attributes.
    """
    name: Optional[str] = Field(None, title="Document Name", description="The name of the document")
    file_path: Optional[str] = Field(None, title="File Path", description="The file path of the document")
    processed_at: Optional[datetime] = Field(None, title="Processed At", description="The timestamp when the document was processed")
    is_processed: Optional[bool] = Field(None, title="Is Processed", description="Indicates whether the document has been processed")

class Document(DocumentBase):
    """
    Represents a document with its unique identifier.
    
    Inherits:
        DocumentBase: Base schema for document attributes.
    
    Attributes:
        id (int): The unique identifier of the document.
    """
    id: int

