from pydantic import BaseModel, Field
from typing import List, Optional

class SourceItem(BaseModel):
    document: str
    page: int
    score: float
    department: Optional[str] = "General"

class ChatMessageRequest(BaseModel):
    question: str = Field(..., min_length=1)
    chat_id: Optional[str] = None
    department_filter: Optional[str] = None

class ChatMessageResponse(BaseModel):
    chat_id: str
    question: str
    answer: str
    sources: List[SourceItem]
    relevance_score: float
    created_at: str

class ChatHistoryItem(BaseModel):
    id: str
    user_id: str
    title: str
    messages: List[dict]
    created_at: str
    updated_at: str
