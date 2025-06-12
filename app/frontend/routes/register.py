# frontend/routes/register.py

# Import necessary modules
from nicegui import ui                                                  # Import the ui module
from frontend.components.navbar import navbar                           # Importing the navbar component
from frontend.components.forms import register_card                     # Importing the register_card component
from frontend.components.header_links import header_links               # Importing the header_links component

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
