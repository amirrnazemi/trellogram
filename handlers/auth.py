# handlers/auth.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from models.user import User
from services.trello_service import TrelloClient
from models.map_list import Map_List
from models.map_card import Map_Card
from config import TRELLO_API_KEY, TRELLO_TOKEN
from aiogram.utils.keyboard import InlineKeyboardBuilder

auth_router = Router()

@auth_router.message(Command("boards"))
async def show_boards(message: types.Message, user: User):
    trello_user_id = user.trello_user_id
    if not trello_user_id:
        await message.answer("شناسه ترلو شما ثبت نشده است.")
        return
    
    trello_client = TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)
    boards = await trello_client.get_boards(user_id=trello_user_id)
    if not boards:
        await message.answer("بردی یافت نشد.")
        return
    
    keyboard = []
    for board in boards:
        keyboard.append([types.InlineKeyboardButton(text=board['name'], callback_data=f"show_lists:{board['id']}")])
    keyboard = InlineKeyboardBuilder(keyboard).as_markup()
    await message.answer("لیست بردهای شما:", reply_markup=keyboard)

# مثال: ایجاد یک نقشه لیست
@auth_router.callback_query(F.data.startswith("show_lists:"))
async def show_lists(callback_query: types.CallbackQuery, user: User):
    board_id = callback_query.data.split(":")[1]
    
    trello_client = TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)
    lists = await trello_client.get_lists(board_id=board_id)
    
    if not lists:
        await callback_query.message.answer("لیستی یافت نشد.")
        return
    
    keyboard = []
    for lst in lists:
        keyboard.append([types.InlineKeyboardButton(text=lst['name'], callback_data=f"map_list:{lst['id']}")])
    keyboard = InlineKeyboardBuilder(keyboard).as_markup()
    await callback_query.message.answer("لیست‌های این برد:", reply_markup=keyboard)

@auth_router.callback_query(F.data.startswith("map_list:"))
async def map_list(callback_query: types.CallbackQuery, user: User):
    list_id = callback_query.data.split(":")[1]
    
    # فرض می‌کنیم که دسته‌بندی مورد نظر کاربر را دریافت کرده‌ایم (برای ساده‌سازی ثابت می‌گذاریم)
    mapped_category = "Default Category"
    
    # ذخیره نقشه لیست
    map_list = await Map_List.find_one(Map_List.trello_list_id == list_id)
    if not map_list:
        map_list = Map_List(name='test', trello_list_id=list_id, mapped_category=mapped_category)
    else:
        map_list.mapped_category = mapped_category
    await map_list.save()
    
    await callback_query.message.answer(f"لیست `{list_id}` به دسته‌بندی `{mapped_category}` نگاشت شد.")
