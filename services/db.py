from mongoengine import connect
from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_NAME, MONGO_URI


async def connect_db():
    
    # اتصال به MongoDB
    connect(DATABASE_NAME)


def get_mongo_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(MONGO_URI)
    return client