from typing import Any, Dict, Optional
import os
import motor.motor_asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow()
    data_with_meta = {
        **data,
        "created_at": now,
        "updated_at": now,
    }
    result = await db[collection_name].insert_one(data_with_meta)
    inserted = await db[collection_name].find_one({"_id": result.inserted_id})
    if inserted and "_id" in inserted:
        inserted["id"] = str(inserted.pop("_id"))
    return inserted or {}

async def get_documents(
    collection_name: str,
    filter_dict: Optional[Dict[str, Any]] = None,
    limit: int = 50,
) -> list[Dict[str, Any]]:
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    items = []
    async for doc in cursor:
        if "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items
