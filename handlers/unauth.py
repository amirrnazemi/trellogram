# handlers/unauth.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F

from states.registration import RegistrationStates
from config import REGISTRATION_PASSWORD, TRELLO_API_KEY, TRELLO_TOKEN
from services.trello_service import TrelloClient
from models.user import User

unauth_router = Router()

@unauth_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        await message.answer("لطفاً رمز عبور اولیه را وارد کنید:")
        await state.set_state(RegistrationStates.waiting_for_password)
    else:
        await message.answer("شما قبلاً ثبت‌نام کرده‌اید.")

@unauth_router.message(RegistrationStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    if message.text == REGISTRATION_PASSWORD:
        await message.answer("رمز عبور صحیح است. در حال دریافت لیست کاربران ترلو شما...")
        await state.set_state(RegistrationStates.choosing_trello_user)
        
        trello_client = TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)
        trello_users = await trello_client.get_members()
        
        if not trello_users:
            await message.answer("لیست کاربران ترلو یافت نشد.")
            await state.clear()
            return
        
        keyboard = types.InlineKeyboardMarkup()
        for user in trello_users:
            username = user.get('username') or user.get('fullName') or "Unknown"
            trello_id = user.get('id')
            keyboard.add(types.InlineKeyboardButton(text=username, callback_data=f"choose_user:{trello_id}"))
        
        await message.answer("لطفاً شناسه ترلو خود را انتخاب کنید:", reply_markup=keyboard)
    else:
        await message.answer("رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.")

@unauth_router.callback_query(F.data.startswith("choose_user:"))
async def process_trello_user(callback_query: CallbackQuery, state: FSMContext):
    trello_user_id = callback_query.data.split(":")[1]
    
    # ذخیره شناسه ترلو در دیتابیس با استفاده از Beanie
    user = await User.find_one(User.telegram_id == str(callback_query.from_user.id))
    if not user:
        user = User(telegram_id=str(callback_query.from_user.id), trello_user_id=trello_user_id, email=f"user{callback_query.from_user.id}@example.com")
    else:
        user.trello_user_id = trello_user_id
    await user.save()

    await callback_query.message.answer(f"شناسه ترلو شما `{trello_user_id}` ثبت شد.")
    await state.clear()
