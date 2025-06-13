# frontend/components/navbar.py

# Import necesary modules
from nicegui import ui                                                  # Import the ui module
from frontend.components.utils.navbar_buttons import navbar_buttons     # Importing the navbar_buttons component

# ----------------------------------------------------------------------------------------------------------------------------------------- #

def go_to(route):
    ui.navigate.to(route)

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
        img.on('click', go_to('/'))
        
        # Second row
        with ui.row().classes('space-x-4'):
            
            # Add the buttons depending on the logged state
            await navbar_buttons()

# ----------------------------------------------------------------------------------------------------------------------------------------- #