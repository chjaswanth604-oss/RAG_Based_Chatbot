import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from services.vector_service import query_vector_db
from services.llm_service import generate_llm_answer

load_dotenv()

logger = logging.getLogger(__name__)

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
TOP_K = int(os.getenv("TOP_K", "4"))

UNANSWERABLE_RESPONSE = "I couldn't find this information in the college knowledge base. Please contact the concerned college department for accurate information."

def execute_rag_pipeline(
    question: str,
    department_filter: Optional[str] = None,
    top_k: int = TOP_K,
    similarity_threshold: float = SIMILARITY_THRESHOLD
) -> Dict[str, Any]:
    """
    Executes full RAG workflow:
    1. Query ChromaDB for top K similar document chunks.
    2. Check similarity scores against SIMILARITY_THRESHOLD.
    3. If max score < threshold, return unknown response with no sources.
    4. Otherwise build context, prompt LLM, and return answer with source citations.
    """
    logger.info(f"Executing RAG pipeline for query: '{question}' (dept: {department_filter})")

    # Step 1: Retrieve top chunks from vector database
    chunks = query_vector_db(query_text=question, top_k=top_k, department_filter=department_filter)

    if not chunks:
        logger.info("No chunks retrieved from ChromaDB.")
        return {
            "answer": UNANSWERABLE_RESPONSE,
            "sources": [],
            "relevance_score": 0.0
        }

    # Step 2: Filter by similarity threshold
    valid_chunks = [c for c in chunks if c["score"] >= similarity_threshold]

    if not valid_chunks:
        highest_score = max([c["score"] for c in chunks]) if chunks else 0.0
        logger.info(f"Max score ({highest_score}) is below threshold ({similarity_threshold}).")
        return {
            "answer": UNANSWERABLE_RESPONSE,
            "sources": [],
            "relevance_score": highest_score
        }

    # Highest score achieved
    max_relevance_score = max([c["score"] for c in valid_chunks])

    # Step 3: Build context string for LLM
    context_blocks = []
    sources_dict = {}

    for c in valid_chunks:
        doc_name = c["document_name"]
        page_num = c["page_number"]
        dept = c["department"]
        score = c["score"]

        context_blocks.append(
            f"--- Document: {doc_name} (Page {page_num}, Dept: {dept}) ---\n{c['text']}"
        )

        # Deduplicate sources by document & page
        src_key = f"{doc_name}_p{page_num}"
        if src_key not in sources_dict or score > sources_dict[src_key]["score"]:
            sources_dict[src_key] = {
                "document": doc_name,
                "page": page_num,
                "score": score,
                "department": dept
            }

    combined_context = "\n\n".join(context_blocks)

    # Step 4: Generate LLM Answer
    answer_text = generate_llm_answer(question=question, context=combined_context)

    sources_list = list(sources_dict.values())
    sources_list.sort(key=lambda x: x["score"], reverse=True)

    return {
        "answer": answer_text,
        "sources": sources_list,
        "relevance_score": max_relevance_score
    }
