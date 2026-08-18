"""
Admin states using FSM
"""
from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    """States for admin operations"""
    
    # Application management states
    waiting_for_application_id = State()
    waiting_for_new_status = State()
    waiting_for_status_notes = State()
    
    # User management states
    waiting_for_user_id = State()
    waiting_for_new_role = State()
    
    # Broadcast states
    waiting_for_broadcast_message = State()
