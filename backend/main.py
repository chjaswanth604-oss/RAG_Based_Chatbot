import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.mongodb import init_db
from database.chromadb import get_collection
from routes.auth import router as auth_router
from routes.chat import router as chat_router
from routes.documents import router as doc_router
from routes.feedback import router as feedback_router
from routes.admin import router as admin_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing RAG College Chatbot backend...")
    await init_db()
    # Initialize ChromaDB collection
    get_collection()
    logger.info("Backend services ready!")
    yield
    logger.info("Shutting down backend...")

app = FastAPI(
    title="RAG College Information Assistant API",
    description="Backend API for document embedding, vector retrieval, and LLM synthesis.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production domain in Vercel/Render deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(doc_router)
app.include_router(feedback_router)
app.include_router(admin_router)

@app.get("/")
@app.get("/api/health")
@app.get("/health")
async def root():
    return {
        "status": "online",
        "service": "RAG-Based College Information Assistant",
        "version": "1.0.0",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

