# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                  # Importing ui from nicegui
from frontend.components.utils import navbar, header_links              # Importing the utils components
from frontend.components.diary import diary_card                        # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth  # Importing the AuthService instance

# ----------------------------------------------------------------------------------------------------------------------------------------- #
@auth.auth_required()
async def create_events_page():
    """ Creates the events page """
    # Build UI
    header_links()
    navbar()
    