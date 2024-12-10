import asyncio
from models import User, init_models

async def test_user():
    await init_models()

    # ایجاد یک کاربر جدید
    user = User(telegram_id="12345", email="test@example.com", is_active=True)
    await user.insert()
    print("User created.")

    # جستجوی کاربر
    user = await User.find_one(User.telegram_id == "12345")
    print(f"User found: {user.model_dump()}")

asyncio.run(test_user())
