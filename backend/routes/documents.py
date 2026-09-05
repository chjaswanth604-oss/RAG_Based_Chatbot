import os
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from models.document import DocumentResponse
from services.document_service import process_document
from services.vector_service import add_chunks_to_vector_db, delete_document_chunks_from_vector_db
from database.mongodb import get_db
from middleware.auth import require_admin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["Documents"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    department: str = Form("General"),
    current_admin: dict = Depends(require_admin)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    doc_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    saved_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")

    with open(saved_path, "wb") as f:
        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )
        f.write(content)

    db = get_db()
    docs_col = db.get_collection("documents")

    doc_record = {
        "_id": doc_id,
        "document_name": file.filename,
        "department": department.strip(),
        "file_path": saved_path,
        "upload_date": now_iso,
        "page_count": 0,
        "chunks_count": 0,
        "status": "Processing",
        "error_message": None
    }
    await docs_col.insert_one(doc_record)

    try:
        page_count, chunks = process_document(
            file_path=saved_path,
            doc_id=doc_id,
            doc_name=file.filename,
            department=department
        )

        indexed_count = add_chunks_to_vector_db(chunks)

        status_str = "Processed" if indexed_count > 0 else "Failed"
        err_msg = None if indexed_count > 0 else "No readable text extracted from document."

        await docs_col.update_one(
            {"_id": doc_id},
            {"$set": {
                "page_count": page_count,
                "chunks_count": indexed_count,
                "status": status_str,
                "error_message": err_msg
            }}
        )

        return DocumentResponse(
            id=doc_id,
            document_name=file.filename,
            department=department,
            upload_date=now_iso,
            page_count=page_count,
            chunks_count=indexed_count,
            status=status_str,
            error_message=err_msg
        )

    except Exception as e:
        logger.error(f"Failed to process document {file.filename}: {e}")
        await docs_col.update_one(
            {"_id": doc_id},
            {"$set": {
                "status": "Failed",
                "error_message": str(e)
            }}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

@router.get("", response_model=List[DocumentResponse])
async def list_documents(current_admin: dict = Depends(require_admin)):
    db = get_db()
    docs_col = db.get_collection("documents")
    cursor = docs_col.find({}).sort("upload_date", -1)
    docs_list = await cursor.to_list(length=200)

    result = []
    for d in docs_list:
        result.append(DocumentResponse(
            id=d["_id"],
            document_name=d.get("document_name", "Unnamed"),
            department=d.get("department", "General"),
            upload_date=d.get("upload_date", ""),
            page_count=d.get("page_count", 0),
            chunks_count=d.get("chunks_count", 0),
            status=d.get("status", "Processed"),
            error_message=d.get("error_message")
        ))
    return result

@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    current_admin: dict = Depends(require_admin)
):
    db = get_db()
    docs_col = db.get_collection("documents")

    doc = await docs_col.find_one({"_id": doc_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Remove file from disk
    if os.path.exists(doc.get("file_path", "")):
        try:
            os.remove(doc["file_path"])
        except Exception as e:
            logger.warning(f"Failed to remove file from disk: {e}")

    # Remove vectors from ChromaDB
    delete_document_chunks_from_vector_db(doc_id)

    # Delete record from MongoDB
    await docs_col.delete_one({"_id": doc_id})

    return {"status": "success", "message": f"Document '{doc.get('document_name')}' deleted successfully."}

@router.put("/{doc_id}", response_model=DocumentResponse)
async def replace_document(
    doc_id: str,
    file: UploadFile = File(...),
    department: str = Form("General"),
    current_admin: dict = Depends(require_admin)
):
    # First delete existing vector chunks and file
    await delete_document(doc_id=doc_id, current_admin=current_admin)
    # Upload as new file
    return await upload_document(file=file, department=department, current_admin=current_admin)
