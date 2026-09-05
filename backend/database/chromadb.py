import os
import logging
import chromadb
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
raw_path = os.getenv("CHROMA_DB_PATH", "chroma_db")
if not os.path.isabs(raw_path):
    # Strip leading ./ or ../ to get clean folder name
    clean_name = raw_path.replace("./", "").replace("../", "")
    CHROMA_DB_PATH = os.path.join(BASE_DIR, clean_name)
else:
    CHROMA_DB_PATH = raw_path

COLLECTION_NAME = "college_knowledge_base"

chroma_client = None
collection = None

def get_chroma_client():
    global chroma_client
    if chroma_client is None:
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        logger.info(f"Initialized ChromaDB persistent client at {CHROMA_DB_PATH}")
    return chroma_client

def get_collection():
    global collection
    if collection is None:
        client = get_chroma_client()
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={
                "description": "College Knowledge Base document vector chunks",
                "hnsw:space": "cosine"
            }
        )
        logger.info(f"ChromaDB collection '{COLLECTION_NAME}' (cosine space) ready.")
    return collection
