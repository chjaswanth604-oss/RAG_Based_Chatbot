import os
import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "college_rag_db")

class MemoryDatabase:
    """Fallback in-memory MongoDB-compatible store when MongoDB server is unavailable."""
    def __init__(self):
        self.users = {}
        self.chats = {}
        self.documents = {}
        self.feedback = []
        logger.warning("Using MemoryDatabase fallback (MongoDB not connected).")

    class AsyncCollection:
        def __init__(self, data_store: dict | list, is_list=False):
            self._store = data_store
            self._is_list = is_list

        async def find_one(self, filter_dict):
            if self._is_list:
                for item in self._store:
                    if all(item.get(k) == v for k, v in filter_dict.items()):
                        return item
                return None
            for key, item in self._store.items():
                if all(item.get(k) == v for k, v in filter_dict.items()):
                    return item
            return None

        async def insert_one(self, doc):
            doc_id = doc.get("_id", str(len(self._store) + 1))
            doc["_id"] = doc_id
            if self._is_list:
                self._store.append(doc)
            else:
                self._store[doc_id] = doc
            class InsertResult:
                inserted_id = doc_id
            return InsertResult()

        def find(self, filter_dict=None):
            filter_dict = filter_dict or {}
            results = []
            source = self._store if self._is_list else self._store.values()
            for item in source:
                if all(item.get(k) == v for k, v in filter_dict.items()):
                    results.append(item)
            class AsyncCursor:
                def __init__(self, data):
                    self._data = data
                def sort(self, key, direction=-1):
                    reverse = direction == -1
                    self._data.sort(key=lambda x: x.get(key, ""), reverse=reverse)
                    return self
                async def to_list(self, length=None):
                    return self._data[:length] if length else self._data
            return AsyncCursor(results)

        async def delete_one(self, filter_dict):
            if self._is_list:
                for idx, item in enumerate(self._store):
                    if all(item.get(k) == v for k, v in filter_dict.items()):
                        self._store.pop(idx)
                        class DeleteResult:
                            deleted_count = 1
                        return DeleteResult()
            else:
                for k, v in list(self._store.items()):
                    if all(v.get(key) == val for key, val in filter_dict.items()):
                        del self._store[k]
                        class DeleteResult:
                            deleted_count = 1
                        return DeleteResult()
            class DeleteResult:
                deleted_count = 0
            return DeleteResult()

        async def update_one(self, filter_dict, update_dict):
            doc = await self.find_one(filter_dict)
            if doc and "$set" in update_dict:
                doc.update(update_dict["$set"])
                class UpdateResult:
                    modified_count = 1
                return UpdateResult()
            class UpdateResult:
                modified_count = 0
            return UpdateResult()

        async def count_documents(self, filter_dict=None):
            filter_dict = filter_dict or {}
            source = self._store if self._is_list else self._store.values()
            count = 0
            for item in source:
                if all(item.get(k) == v for k, v in filter_dict.items()):
                    count += 1
            return count

    def get_collection(self, name: str):
        if name == "users":
            return self.AsyncCollection(self.users)
        elif name == "chats":
            return self.AsyncCollection(self.chats)
        elif name == "documents":
            return self.AsyncCollection(self.documents)
        elif name == "feedback":
            return self.AsyncCollection(self.feedback, is_list=True)
        return self.AsyncCollection({})

client: Optional[AsyncIOMotorClient] = None
db = None
use_memory_fallback = False
memory_db: Optional[MemoryDatabase] = None

async def init_db():
    global client, db, use_memory_fallback, memory_db
    try:
        client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        # Verify connection
        await client.server_info()
        db = client[DB_NAME]
        logger.info(f"Connected to MongoDB at {MONGO_URI}, database: {DB_NAME}")
    except Exception as e:
        logger.warning(f"MongoDB connection failed ({e}). Falling back to memory database.")
        use_memory_fallback = True
        memory_db = MemoryDatabase()

def get_db():
    if use_memory_fallback or db is None:
        if memory_db is None:
            return MemoryDatabase()
        return memory_db
    return db
