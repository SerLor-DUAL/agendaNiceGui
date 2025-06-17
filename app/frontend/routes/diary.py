# frontend/routes/diary.py

# Import necessary modules
from nicegui import ui                                                  # Importing ui from nicegui
from frontend.components.diary import DiaryCard                         # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth  # Importing the AuthService instance
from frontend.services.event_services import EventService as es         # Importing EventService for comm with Back

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Decorator that checks authorization
@auth.auth_required()
async def create_diary_page():
    """ Function to create the calendar page """
    # I don't like it but as it is an object, it must be done this way.
    # Can't use async methods inside it.
    events_service = es()
    events = await events_service.get_events()
    dc = DiaryCard(events)
    dc.create_diary_card()