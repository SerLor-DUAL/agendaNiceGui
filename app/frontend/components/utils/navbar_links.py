# frontend/components/navbar_links.py

# Import necesary modules
from nicegui import ui                                                      # Import the ui module
from frontend.services.auth_services import front_auth_service as auth      # Importing the AuthService instance
from frontend.utils.routing import front_router_handler as frh              # Importing the RouteHandler

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Styles for the desktop links
desktop_link_classes = (
                            'text-white no-underline '
                            'hover:text-blue-300 hover:underline '
                            'transition-colors duration-200 '
                            'text-base font-medium px-3 py-2 rounded-md '
                            'whitespace-nowrap'
                        )

# Styles for mobile links (botones que parecen links)
mobile_link_classes = (
                            'text-white hover:text-blue-300 hover:bg-gray-800 '
                            'text-lg px-4 py-1 rounded-lg '
                            'w-full text-left transition-all duration-200 '
                            'bg-transparent border-none font-medium '
                            'flex items-center justify-start no-underline'
                        )
            
# NOTE: Function to add the navbar links component for desktop
async def navbar_links(current_user):
    #If user is logged in show diary and events links
    # if logged:
    if current_user:
        ui.link('Diario', '/diary').classes(desktop_link_classes)

# NOTE: Function to add the navbar links component for mobile
async def mobile_nav_links(current_user):
    #If user is logged in show calendar and events links
    # if logged:
    if current_user:
        ui.link('Diario', '/diary').classes(mobile_link_classes)