from .user import User
from .map_list import Map_List
from .map_card import Map_Card

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# تابع برای راه‌اندازی Beanie
async def init_models(mongo_client: AsyncIOMotorClient):
    await init_beanie(database=mongo_client.get_default_database(), document_models=[User, Map_List, Map_Card])