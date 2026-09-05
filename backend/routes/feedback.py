import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from models.feedback import FeedbackRequest, FeedbackResponse
from database.mongodb import get_db
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

@router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    payload: FeedbackRequest,
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    feedback_col = db.get_collection("feedback")

    feedback_doc = {
        "_id": str(uuid.uuid4()),
        "user_id": current_user["_id"],
        "chat_id": payload.chat_id,
        "question": payload.question,
        "answer": payload.answer,
        "feedback": payload.feedback,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    await feedback_col.insert_one(feedback_doc)

    return FeedbackResponse(
        status="success",
        message="Thank you for your feedback!"
    )
