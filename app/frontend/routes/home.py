# frontend/routes/home.py

# Import necessary modules
from nicegui import ui

async def create_home_page():
    """Creates the home page"""
    ui.add_head_html('<link rel="stylesheet" href="/static/css/animations.css">')
    # Principal container
    with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-[1.1fr_0.9fr] xl:grid-cols-[0.8fr_1.2fr] gap-8 w-full md:h-[80vh] sm:h-[50vh] p-8 items-center md:pt-8'):
        
        # Text left column
        with ui.element('div').classes(
            'flex flex-col h-full justify-center items-center text-center md:text-left order-2 md:order-1 md:pt-8'
        ):
            
            ui.label('AgendaNiceGUI').classes(
                'text-4xl md:text-7xl font-bold text-gray-900 mb-6 slide-in-left'
            ).style('animation-delay: 0.1s;')

            ui.label('Esta agenda es nuestra brújula.🧭').classes(
                'text-xl md:text-3xl text-gray-700 slide-in-left'
            ).style('animation-delay: 0.1s;')

        # Image right column
        with ui.element('div').classes(
            'flex justify-center w-full h-full items-start order-1 md:order-2 md:pt-8'
        ):
            with ui.element('div').classes('w-full self-start 2xl:self-end'):
                ui.image('/static/img/hero.png').classes(
                    'w-full h-auto max-w-[800px] max-h-[70vh] object-contain rounded-2xl mx-auto'
                )
