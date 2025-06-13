# frontend/components/navbar.py

# Import necesary modules
from nicegui import ui                                                  # Import the ui module
from frontend.components.utils.navbar_buttons import navbar_buttons     # Importing the navbar_buttons component
from frontend.utils.routing import front_router_handler as frh          # Importing the RouteHandler

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to add the navbar component
async def navbar():
    
    # Principal row
    with ui.row().classes('items-center justify-between bg-gray-800 p-4 text-white w-full rounded-t'):
        
        # Logo image
        img = ui.image('/static/img/logo.png').classes(
                                                        'w-16 h-auto rounded '
                                                        'cursor-pointer ' 
                                                        'hover:opacity-80 '
                                                        'transition-opacity duration-300' 
                                                        )
        
        # Logo click event
        img.on('click', lambda: frh.go_to('/'))
        
        # Second row
        with ui.row().classes('space-x-4'):
            
            # Add the buttons depending on the logged state
            await navbar_buttons()

# ----------------------------------------------------------------------------------------------------------------------------------------- #