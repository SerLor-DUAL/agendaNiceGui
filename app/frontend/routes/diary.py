# frontend/routes/diary.py

# Import necessary modules
from nicegui import ui                                                  # Importing ui from nicegui
from frontend.components.diary import DiaryCard                         # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth  # Importing the AuthService instance

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Decorator that checks authorization
@auth.auth_required()
async def create_diary_page():
    """ Function to create the calendar page """

    dc = DiaryCard()
    dc.create_diary_card()