# frontend/routes/register.py

# Import necessary modules
from nicegui import ui                                                  # Import the ui module
from frontend.components.utils import navbar, header_links              # Importing the utils components
from frontend.components.forms import register_card                     # Importing the register_card component

# ----------------------------------------------------------------------------------------------------------------------------------------- #

@ui.page('/register')
def create_register_page():
    """ Creates the register page """
    
    # Header links
    header_links()

    # Principal row
    with ui.column().classes('w-full h-screen bg-gray-100'):
        
        # Navbar
        navbar()
        
        # Register card
        register_card()