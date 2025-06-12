# frontend/routes/login.py

# Import necessary modules
from nicegui import ui                                                          # Import the ui module
from frontend.components.navbar import navbar                                   # Importing the navbar component
from frontend.components.forms import login_card                                # Importing the login_card component
from frontend.components.header_links import header_links                       # Importing the header_links component

# ----------------------------------------------------------------------------------------------------------------------------------------- #

@ui.page('/login')
def create_login_page():
    """ Creates the login page """
    
    # Header links
    header_links()
    
    # Login form
    with ui.column().classes('w-full h-screen bg-gray-100'):
        
        # Navbar
        navbar()
        
        # Centered row
        with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
            
            # Login card
            login_card()
            