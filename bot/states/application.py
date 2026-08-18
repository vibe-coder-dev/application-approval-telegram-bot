"""
Application form states using FSM
"""
from aiogram.fsm.state import State, StatesGroup


class ApplicationState(StatesGroup):
    """States for application creation process"""
    
    # Main states
    waiting_for_service_type = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_file = State()
    waiting_for_confirmation = State()
    
    # Sub-states for file upload
    waiting_for_file_type = State()
    waiting_for_photo = State()
    waiting_for_document = State()
    
    # State for viewing applications
    viewing_applications = State()
    viewing_application_detail = State()
    
    # State for language selection
    waiting_for_language = State()
