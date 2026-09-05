import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from models.chat import ChatMessageRequest, ChatMessageResponse, SourceItem
from services.rag_service import execute_rag_pipeline
from database.mongodb import get_db
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("", response_model=ChatMessageResponse)
async def send_chat_message(
    payload: ChatMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["_id"]
    question = payload.question.strip()
    chat_id = payload.chat_id or str(uuid.uuid4())
    dept_filter = payload.department_filter

    # Execute RAG pipeline
    rag_result = execute_rag_pipeline(
        question=question,
        department_filter=dept_filter
    )

    now_iso = datetime.now(timezone.utc).isoformat()

    msg_entry = {
        "msg_id": str(uuid.uuid4()),
        "question": question,
        "answer": rag_result["answer"],
        "sources": rag_result["sources"],
        "relevance_score": rag_result["relevance_score"],
        "created_at": now_iso
    }

    db = get_db()
    chats_col = db.get_collection("chats")

    existing_chat = await chats_col.find_one({"_id": chat_id, "user_id": user_id})

    if existing_chat:
        messages = existing_chat.get("messages", [])
        messages.append(msg_entry)
        await chats_col.update_one(
            {"_id": chat_id},
            {"$set": {"messages": messages, "updated_at": now_iso}}
        )
    else:
        title = question[:40] + "..." if len(question) > 40 else question
        new_chat_doc = {
            "_id": chat_id,
            "user_id": user_id,
            "title": title,
            "messages": [msg_entry],
            "created_at": now_iso,
            "updated_at": now_iso
        }
        await chats_col.insert_one(new_chat_doc)

    sources_obj = [SourceItem(**s) for s in rag_result["sources"]]

    return ChatMessageResponse(
        chat_id=chat_id,
        question=question,
        answer=rag_result["answer"],
        sources=sources_obj,
        relevance_score=rag_result["relevance_score"],
        created_at=now_iso
    )

@router.get("/history")
async def get_chat_history(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    db = get_db()
    chats_col = db.get_collection("chats")
    cursor = chats_col.find({"user_id": user_id}).sort("updated_at", -1)
    chats_list = await cursor.to_list(length=100)

    result = []
    for c in chats_list:
        result.append({
            "id": c["_id"],
            "title": c.get("title", "Conversation"),
            "created_at": c.get("created_at", ""),
            "updated_at": c.get("updated_at", ""),
            "message_count": len(c.get("messages", []))
        })
    return result

@router.get("/{chat_id}")
async def get_chat_detail(
    chat_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["_id"]
    db = get_db()
    chats_col = db.get_collection("chats")
    chat = await chats_col.find_one({"_id": chat_id, "user_id": user_id})
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat thread not found"
        )
    return {
        "id": chat["_id"],
        "title": chat.get("title", "Conversation"),
        "messages": chat.get("messages", []),
        "created_at": chat.get("created_at", ""),
        "updated_at": chat.get("updated_at", "")
    }

@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["_id"]
    db = get_db()
    chats_col = db.get_collection("chats")
    res = await chats_col.delete_one({"_id": chat_id, "user_id": user_id})
    if res.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat thread not found or already deleted"
        )
    return {"status": "success", "message": "Chat thread deleted"}
