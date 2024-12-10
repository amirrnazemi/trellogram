from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from models import User

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = None
        if isinstance(event, Message) and event.from_user:
            user_id = str(event.from_user.id)
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = str(event.from_user.id)
        
        if user_id:
            try:         
                data['user'] = await User.find_one(User.telegram_id == user_id)
            except AttributeError:
                data['user'] = None
        else:
            data['user'] = None
        
        return await handler(event, data)
