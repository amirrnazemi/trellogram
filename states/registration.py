# states/registration.py

from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    waiting_for_password = State()
    choosing_trello_user = State()
