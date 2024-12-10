# clear_collections.py

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

async def clear_collections():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_default_database()
    await db.drop_collection("users")
    await db.drop_collection("map_lists")
    await db.drop_collection("map_cards")
    await db.drop_collection("aiogram_fsm")  # اگر نیاز به پاک‌سازی وضعیت‌های FSM دارید
    print("کالکشن‌ها پاک‌سازی شدند.")

if __name__ == "__main__":
    asyncio.run(clear_collections())
