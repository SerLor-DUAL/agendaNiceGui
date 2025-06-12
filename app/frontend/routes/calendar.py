# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                  # Importing ui from nicegui
from frontend.components.navbar import navbar                           # Importing the navbar component
from frontend.components.header_links import header_links               # Importing the header_links component
from frontend.components.diary import diary_card                        # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth  # Importing the AuthService instance
import httpx                                                            # Importing httpx for making HTTP requests

# ----------------------------------------------------------------------------------------------------------------------------------------- #
@auth.auth_required()
async def create_calendar_page():
    
    # result = await auth.get_me()

    # if not result.get('success', False):
    #     ui.notify('You are not logged in. Redirecting to login...', color='negative')
    #     ui.navigate.to('/login')
    #     return

    # Construye UI
    header_links()
    navbar()
    diary_card()