from pydantic import BaseModel, Field
from typing import Literal

class FeedbackRequest(BaseModel):
    chat_id: str
    question: str
    answer: str
    feedback: Literal["thumbs_up", "thumbs_down"]

class FeedbackResponse(BaseModel):
    status: str
    message: str
