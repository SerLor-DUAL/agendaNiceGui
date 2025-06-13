# frontend/routes/login.py

# Import necessary modules
from nicegui import ui                                                          # Import the ui module
from frontend.components.utils import navbar, header_links                      # Importing the utils components
from frontend.components.forms import login_card                                # Importing the login_card component

# ----------------------------------------------------------------------------------------------------------------------------------------- #

@ui.page('/login')
async def create_login_page():
    """ Creates the login page """
    
    # Header links
    header_links()
    
    # Login form
    with ui.column().classes('w-full h-screen bg-gray-100'):
        
        # Navbar
        await navbar()
        
        # Centered row
        with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
            
            # Login card
            login_card()
            