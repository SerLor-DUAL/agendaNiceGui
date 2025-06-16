# frontend/routes/logout.py

# Importing necessary modules
from nicegui import ui                                                    # Import the ui module
from frontend.services.auth_services import front_auth_service as auth    # Import the AuthService instance
from frontend.utils.routing import front_router_handler as frh            # Importing the RouteHandler

async def create_logout_page():
    
    # Closes the session, clears the local cache and cookies
    await auth.logout()
    
    # Redirects to the home page
    frh.go_to('/')
    
    
    