from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI


def get_mongo_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(MONGO_URI)
    return client