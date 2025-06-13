# frontend/routes/home.py

# Import necessary modules
from nicegui import ui                                                  # Import the ui module
from frontend.components.utils import navbar, header_links              # Importing the utils components

# ----------------------------------------------------------------------------------------------------------------------------------------- #

@ui.page('/home')
async def create_home_page():
    """ Creates the home page """
    
    # Header links
    header_links()
    
    # Navbar
    await navbar()
    
    # Principal row
    with ui.row().classes('flex items-center justify-between h-[80%] px-8 bg-gray-50 w-full'):

        # Left column
        with ui.column().classes('flex-1 pr-8 text-center h-full'):
            
            # Title
            ui.label('AgendaNiceGUI').classes('text-4xl md:text-6xl lg:text-8xl font-bold text-gray-900 mb-12 w-full slide-in-left').style('animation-delay: 0s;')
            
            # Subtitle
            ui.label('Esta agenda es nuestra brújula. 🧭').classes('!text-3xl text-gray-700 w-full slide-in-left').style('animation-delay: 0s;')

        # Right column
        with ui.column().classes('flex-1 pl-8 text-center md:text-right'):
            
            # Image
            ui.image('/static/img/hero.png').classes('w-[90%] h-[90%] p-4 mx-auto m-4 rounded-xl')
