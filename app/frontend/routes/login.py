# frontend/routes/login.py

from nicegui import ui
from frontend.components.navbar import navbar
from ..components.formCard import login_card
from ..components.headerLinks import header_links
# import httpx

# Function to render the login page
def create_login_page():
    header_links()
    
    # Login form
    with ui.column().classes('w-full h-screen bg-gray-100'):
        
        # Navbar
        navbar()
        
        # Centered row
        with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
            # Login card
            login_card()
            