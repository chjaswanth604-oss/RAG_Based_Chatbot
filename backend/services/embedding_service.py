import os
import logging
from typing import List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading SentenceTransformer model: {EMBEDDING_MODEL_NAME}")
            _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise e
    return _model

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Generates embedding vectors for a list of text strings."""
    if not texts:
        return []
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.tolist()

def generate_query_embedding(query: str) -> List[float]:
    """Generates embedding vector for a single search query."""
    model = get_embedding_model()
    embedding = model.encode(query, show_progress_bar=False, convert_to_numpy=True)
    return embedding.tolist()
