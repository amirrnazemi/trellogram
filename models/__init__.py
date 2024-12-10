from .user import User
from .map_list import Map_List
from .map_card import Map_Card

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI


# تابع برای راه‌اندازی Beanie
async def init_models():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client.get_default_database(), document_models=[User])