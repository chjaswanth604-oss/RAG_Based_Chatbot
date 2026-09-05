import os
import uuid
import logging
from typing import List, Dict, Any, Tuple
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> List[Tuple[int, str]]:
    """
    Extracts text page-by-page from a PDF file using PyMuPDF.
    Returns a list of tuples: (page_number_1_indexed, cleaned_text)
    """
    pages_data = []
    try:
        doc = fitz.open(file_path)
        for page_index in range(len(doc)):
            page = doc[page_index]
            text = page.get_text("text")
            cleaned_text = " ".join(text.split()).strip()
            if cleaned_text:
                pages_data.append((page_index + 1, cleaned_text))
        doc.close()
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {e}")
        raise ValueError(f"Failed to parse PDF document: {str(e)}")
    return pages_data

def extract_text_from_txt(file_path: str) -> List[Tuple[int, str]]:
    """Extracts text from a .txt file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    cleaned = " ".join(text.split()).strip()
    return [(1, cleaned)] if cleaned else []

def extract_text_from_file(file_path: str) -> List[Tuple[int, str]]:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".txt", ".text"]:
        return extract_text_from_txt(file_path)
    elif ext == ".docx":
        try:
            import docx
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text.strip())
            cleaned = " ".join(full_text)
            return [(1, cleaned)] if cleaned else []
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            raise ValueError("Failed to extract DOCX file content.")
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def chunk_text_by_words(
    text: str,
    page_num: int,
    doc_id: str,
    doc_name: str,
    department: str,
    chunk_size_words: int = 400,
    overlap_words: int = 80
) -> List[Dict[str, Any]]:
    """
    Splits text into chunks of specified word length with overlap.
    Retains document metadata on every chunk.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    step = chunk_size_words - overlap_words
    if step <= 0:
        step = chunk_size_words

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size_words]
        chunk_str = " ".join(chunk_words).strip()
        if chunk_str:
            chunks.append({
                "chunk_id": f"{doc_id}_p{page_num}_{uuid.uuid4().hex[:6]}",
                "document_id": doc_id,
                "document_name": doc_name,
                "page_number": page_num,
                "department": department,
                "text": chunk_str
            })
    return chunks

def process_document(
    file_path: str,
    doc_id: str,
    doc_name: str,
    department: str = "General",
    chunk_size_words: int = 400,
    overlap_words: int = 80
) -> Tuple[int, List[Dict[str, Any]]]:
    """
    Processes a document file: extracts text, chunks it with metadata, returns (page_count, chunks_list).
    """
    pages_data = extract_text_from_file(file_path)
    page_count = len(pages_data)
    all_chunks = []

    for page_num, page_text in pages_data:
        chunks = chunk_text_by_words(
            text=page_text,
            page_num=page_num,
            doc_id=doc_id,
            doc_name=doc_name,
            department=department,
            chunk_size_words=chunk_size_words,
            overlap_words=overlap_words
        )
        all_chunks.extend(chunks)

    return page_count, all_chunks
