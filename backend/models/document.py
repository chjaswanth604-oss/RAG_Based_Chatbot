from pydantic import BaseModel
from typing import Optional, Literal

class DocumentResponse(BaseModel):
    id: str
    document_name: str
    department: str
    upload_date: str
    page_count: int
    chunks_count: int
    status: Literal["Processing", "Processed", "Failed"]
    error_message: Optional[str] = None

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    department: str
    text: str
