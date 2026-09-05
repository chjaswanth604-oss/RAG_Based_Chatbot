from fastapi import APIRouter, Depends
from database.mongodb import get_db
from middleware.auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/stats")
async def get_admin_stats(current_admin: dict = Depends(require_admin)):
    db = get_db()
    docs_col = db.get_collection("documents")
    users_col = db.get_collection("users")
    chats_col = db.get_collection("chats")

    total_documents = await docs_col.count_documents({})
    docs_processed = await docs_col.count_documents({"status": "Processed"})
    docs_failed = await docs_col.count_documents({"status": "Failed"})

    total_students = await users_col.count_documents({"role": "student"})

    all_chats = await chats_col.find({}).to_list(length=1000)
    total_questions = sum(len(chat.get("messages", [])) for chat in all_chats)

    return {
        "total_documents": total_documents,
        "total_students": total_students,
        "total_questions": total_questions,
        "documents_processed": docs_processed,
        "processing_failed": docs_failed
    }
