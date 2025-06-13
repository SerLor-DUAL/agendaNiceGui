# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                  # Importing ui from nicegui
from frontend.components.utils import navbar, header_links              # Importing the utils components
from frontend.components.diary import diary_card                        # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth  # Importing the AuthService instance

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