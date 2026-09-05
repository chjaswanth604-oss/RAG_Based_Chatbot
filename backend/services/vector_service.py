import logging
from typing import List, Dict, Any, Optional
from database.chromadb import get_collection
from services.embedding_service import generate_embeddings, generate_query_embedding

logger = logging.getLogger(__name__)

def add_chunks_to_vector_db(chunks: List[Dict[str, Any]]) -> int:
    """
    Ingests document chunks into ChromaDB.
    Each chunk dict must contain:
    - chunk_id, document_id, document_name, page_number, department, text
    """
    if not chunks:
        return 0

    collection = get_collection()
    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [
        {
            "document_id": str(c["document_id"]),
            "document_name": str(c["document_name"]),
            "page_number": int(c["page_number"]),
            "department": str(c.get("department", "General")),
            "chunk_id": str(c["chunk_id"]),
        }
        for c in chunks
    ]

    embeddings = generate_embeddings(texts)

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

    logger.info(f"Successfully indexed {len(chunks)} chunks in ChromaDB.")
    return len(chunks)

def query_vector_db(
    query_text: str,
    top_k: int = 4,
    department_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Queries ChromaDB for top K semantically similar chunks.
    Returns list of dicts with: text, metadata (document_name, page_number, department, etc.), similarity_score (0.0 to 1.0)
    """
    collection = get_collection()
    query_embedding = generate_query_embedding(query_text)

    where_clause = None
    if department_filter and department_filter.strip() and department_filter != "All":
        where_clause = {"department": department_filter}

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )
    except Exception as e:
        logger.warning(f"Filtered query failed ({e}), falling back to unfiltered query.")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

    matched_chunks = []
    if not results or not results["documents"] or not results["documents"][0]:
        return matched_chunks

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(docs, metas, distances):
        # Convert Chroma distance (cosine or L2 distance) to similarity score between 0 and 1
        # For Cosine distance: similarity = 1 - distance
        # For L2: similarity = max(0, 1 - dist / 2)
        score = round(max(0.0, min(1.0, 1.0 - dist)), 4)
        matched_chunks.append({
            "text": doc,
            "document_name": meta.get("document_name", "Unknown Document"),
            "page_number": meta.get("page_number", 1),
            "department": meta.get("department", "General"),
            "document_id": meta.get("document_id", ""),
            "chunk_id": meta.get("chunk_id", ""),
            "score": score,
        })

    return matched_chunks

def delete_document_chunks_from_vector_db(document_id: str) -> bool:
    """Deletes all chunks belonging to a document from ChromaDB."""
    try:
        collection = get_collection()
        collection.delete(where={"document_id": str(document_id)})
        logger.info(f"Deleted vector chunks for document_id: {document_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting chunks for document_id {document_id}: {e}")
        return False
