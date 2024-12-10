# test_beanie.py

import asyncio
from models.user import User, init_models

async def main():
    # راه‌اندازی مدل‌ها و اتصال به دیتابیس
    await init_models()
    
    # ایجاد یک کاربر جدید
    try:
        user1 = User(
            telegram_id="12345",
            trello_user_id="trello_123",
            email="user1@example.com"
        )
        await user1.insert()
        print("User1 created.")
    except Exception as e:
        print(f"Error creating User1: {e}")
    
    # تلاش برای ایجاد کاربری با همان ایمیل (باید خطا بدهد)
    try:
        user2 = User(
            telegram_id="67890",
            trello_user_id="trello_456",
            email="user1@example.com"  # همان ایمیل user1
        )
        await user2.insert()
    except Exception as e:
        print(f"Error creating User2: {e}")  # انتظار می‌رود خطایی مبنی بر یکتایی ایمیل دریافت شود
    
    # # خواندن کاربر
    user = await User.find_one(User.telegram_id == "12345")
    if user:
        print(f"Found user: {user.telegram_id}, Email: {user.email}, Trello ID: {user.trello_user_id}")
    else:
        print("User not found.")
    
    # به‌روزرسانی کاربر
    user.email = "new_email@example.com"
    await user.save()
    print("User1 updated with new email.")
    
    # خواندن مجدد کاربر
    user = await User.find_one(User.telegram_id == "12345")
    if user:
        print(f"Updated user: {user.telegram_id}, Email: {user.email}, Trello ID: {user.trello_user_id}")
    
    # حذف کاربر
    await user.delete()
    await user2.delete()
    print("User1 deleted.")
    
    # بررسی حذف کاربر
    user = await User.find_one(User.telegram_id == "12345")
    if not user:
        print("User1 successfully deleted.")
    else:
        print("Failed to delete User1.")


if __name__ == "__main__":
    asyncio.run(main())
