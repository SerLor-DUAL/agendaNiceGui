# frontend/routes/home.py

# Import necessary modules
from nicegui import ui

async def create_home_page():
    """Creates the home page"""
    
    # Principal container
    with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-[1.1fr_0.9fr] xl:grid-cols-[0.8fr_1.2fr] gap-8 w-full md:h-[80vh] sm:h-[50vh] p-8 items-center md:pt-8'):
        
        # Text left column
        with ui.element('div').classes(
            'flex flex-col h-full justify-start items-center md:items-start text-center md:text-left order-2 md:order-1 md:pt-8'
        ):
            ui.label('AgendaNiceGUI').classes(
                'text-2xl sm:text-3xl md:text-5xl font-bold text-gray-900 mb-6 slide-in-left'
            ).style('animation-delay: 0.1s;')

            ui.label('Esta agenda es nuestra brújula.🧭').classes(
                'text-[14px] sm:text-xl md:text-2xl text-gray-700 slide-in-left'
            ).style('animation-delay: 0.2s;')

        # Image right column
        with ui.element('div').classes(
            'flex justify-center w-full h-full items-start order-1 md:order-2 md:pt-8'
        ):
            with ui.element('div').classes('w-full self-start'):
                ui.image('/static/img/hero.png').classes(
                    'w-full h-auto max-h-[40vh] md:max-h-[52vh] lg:max-h-[72vh] object-contain rounded-xl'
                )
