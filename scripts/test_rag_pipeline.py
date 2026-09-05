import os
import sys
import glob

# Ensure backend directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from services.document_service import process_document
from services.vector_service import add_chunks_to_vector_db, get_collection
from services.rag_service import execute_rag_pipeline

def test_rag_pipeline():
    print("=== 1. Ingesting Sample Documents into Vector DB ===")
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_documents"))
    pdf_files = glob.glob(os.path.join(sample_dir, "*.pdf"))

    print(f"Found {len(pdf_files)} PDF files in {sample_dir}:")
    for pdf_path in pdf_files:
        doc_name = os.path.basename(pdf_path)
        dept = "Electrical Engineering" if "Electrical" in doc_name else ("Computer Science" if "Computer" in doc_name else "General")
        page_count, chunks = process_document(
            file_path=pdf_path,
            doc_id=doc_name.replace(".pdf", ""),
            doc_name=doc_name,
            department=dept
        )
        add_chunks_to_vector_db(chunks)
        print(f"  Indexed: {doc_name} ({page_count} pages, {len(chunks)} chunks)")

    print("\n=== 2. Running Required Verification Test Cases ===")

    test_queries = [
        ("Test 1: Attendance Requirement", "What is the minimum attendance requirement?"),
        ("Test 2: Hostel Timings", "What are the hostel timings?"),
        ("Test 3: Course Fee", "What is the fee for the course?"),
        ("Test 4: Out-of-Domain Question", "What is the capital of France?"),
        ("Test 5: Dept Specific", "What are the electrical engineering lab requirements?")
    ]

    for label, query in test_queries:
        print(f"\n--- {label} ---")
        print(f"Question: {query}")
        result = execute_rag_pipeline(question=query)
        print(f"Relevance Score: {result['relevance_score']}")
        print(f"Answer: {result['answer']}")
        print("Sources:")
        for src in result["sources"]:
            print(f"   Document: {src['document']} (Page {src['page']}, Dept: {src['department']}, Score: {src['score']})")

    print("\n=== RAG Pipeline Verification Complete! ===")

if __name__ == "__main__":
    test_rag_pipeline()
