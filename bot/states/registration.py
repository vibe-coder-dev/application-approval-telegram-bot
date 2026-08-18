"""
Registration states using FSM
"""
from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    """States for user registration process"""
    
    waiting_for_email = State()
    waiting_for_phone = State()
    waiting_for_confirmation = State()
