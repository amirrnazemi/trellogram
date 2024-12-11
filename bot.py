import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.mongo import MongoStorage
import asyncio

from config import BOT_TOKEN
from middlewares.auth_middleware import AuthMiddleware
from handlers.unauth import unauth_router
from handlers.auth import auth_router
from services.db import get_mongo_client
from models import init_models

async def main():

    # اتصال به دیتابیس
    await init_models()

    # راه‌اندازی ربات
    bot = Bot(token=BOT_TOKEN)
    
    # راه‌اندازی MongoStorage
    mongo_client = get_mongo_client()
    storage = MongoStorage(mongo_client)

    dp = Dispatcher(storage=storage)

    # اضافه کردن Middleware
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    # # ثبت روترها
    dp.include_router(unauth_router)
    dp.include_router(auth_router)

    print("BOT started!")

    # شروع ربات
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
