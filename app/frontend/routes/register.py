# frontend/routes/register.py

# Import necessary modules
from nicegui import ui                                                  # Import the ui module
from frontend.components.utils import navbar, header_links              # Importing the utils components
from frontend.components.forms import register_card                     # Importing the register_card component

# ----------------------------------------------------------------------------------------------------------------------------------------- #

@ui.page('/register')
async def create_register_page():
    """ Creates the register page """
    

    # Principal row
    with ui.column().classes('w-full h-screen bg-gray-100'):
        
        
        # Register card
        register_card()