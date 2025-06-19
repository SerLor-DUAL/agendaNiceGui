# frontend/routes/diary.py

# Import necessary modules
from nicegui import ui                                                      # Importing ui from nicegui
from frontend.components.diary import DiaryCard                             # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth      # Importing the AuthService instance
from frontend.services.event_services import front_event_service as es      # Importing the event service      

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Decorator that checks authorization
@auth.auth_required()
async def create_diary_page():
    """ Function to create the calendar page """

    # Load the events from the event service
    # This will fetch the events from the backend API
    events = await es.get_events()
    
    # If there are no events, we show a warning message and initialize events as an empty dictionary
    if events is None:
        print("Advertencia: No hay eventos disponibles.")
        events = {}
    
    # Create the diary card object with the fetched events
    dc = DiaryCard(events)
    
    # Add the diary card to the UI
    dc.create_diary_card()