# handlers/unauth.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder


from states.registration import RegistrationStates
from config import REGISTRATION_PASSWORD, TRELLO_API_KEY, TRELLO_TOKEN
from services.trello_service import TrelloClient
from models.user import User

unauth_router = Router()

@unauth_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext,  **kwargs):
    user : User = kwargs.get('user')
    text = f'سلام {message.from_user.first_name}🙂 \n'
    
    if user:
        text += f'شما قبلا ثبت نام کردی برای اینکه وارد داشبورد بشی از /dashboard استفاده کن.' 
        await message.answer(text)
        await state.clear() 
    else:
        current_state = await state.get_state()
        if not current_state:
            text += "لطفاً رمز عبور اولیه را وارد کنید:"
            await message.answer(text)
            await state.set_state(RegistrationStates.waiting_for_password)
        else:
            text += 'لطفا دوباره با /start شروع کن.'
            await state.clear() 
            await message.answer(text)

@unauth_router.message(Command("restart"))
async def cmd_start(message: types.Message, state: FSMContext,  **kwargs):
    await state.clear()
    await message.answer("استیت ها بازنشانی شدند.")

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
        
        keyboard = []
        for user in trello_users:
            username = user.get('username') or user.get('fullName') or "Unknown"
            trello_id = user.get('id')
            keyboard.append([types.InlineKeyboardButton(text=username, callback_data=f"choose_user:{trello_id}")])
            
        keyboard = InlineKeyboardBuilder(keyboard).as_markup()
        
        await message.answer("لطفاً شناسه ترلو خود را انتخاب کنید:", reply_markup=keyboard)
    else:
        await message.answer("رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.")

@unauth_router.callback_query(F.data.startswith("choose_user:"))
async def process_trello_user(callback_query: CallbackQuery, state: FSMContext, **kwargs):
    trello_user_id = callback_query.data.split(":")[1]
    
    # ذخیره شناسه ترلو در دیتابیس با استفاده از Beanie
    user = kwargs.get('user')
    if not user:
        user = User(telegram_id=str(callback_query.from_user.id), trello_user_id=trello_user_id, email=f"user{callback_query.from_user.id}@example.com")
    else:
        user.trello_user_id = trello_user_id
    print(user)
    await user.save()

    await callback_query.message.answer(f"شناسه ترلو شما `{trello_user_id}` ثبت شد.")
    await state.clear()
