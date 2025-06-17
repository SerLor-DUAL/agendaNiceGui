# frontend/routes/home.py

# Import necessary modules
from nicegui import ui                                                  # Import the ui module
from frontend.components.utils import navbar                            # Importing the utils components
# Importing the AuthService instance
from frontend.services.auth_services import front_auth_service as auth   
# ----------------------------------------------------------------------------------------------------------------------------------------- #

async def create_home_page():
    """ Creates the home page """

    with ui.row().classes(
        'flex flex-col-reverse lg:flex-row items-start justify-end lg:justify-start w-full bg-gray-50 px-4 lg:px-8 py-8 ' +
        'min-h-screen lg:min-h-0 lg:h-[80%]'
    ):
        # Left column
        with ui.column().classes(
            'w-full lg:flex-1 lg:h-full lg:pl-4 text-center lg:text-left lg:self-center'
        ):
            ui.label('AgendaNiceGUI').classes(
                'text-4xl lg:text-6xl xl:text-7xl font-bold text-gray-900 mb-10 lg:mb-12 w-full slide-in-left'
            ).style('animation-delay: 0s;')

            ui.label('Esta agenda es nuestra brújula. 🧭').classes(
                '!text-2xl lg:!text-3xl text-gray-700 w-full slide-in-left'
            ).style('animation-delay: 0.1s;')

        # Right column
        with ui.column().classes(
            'w-full lg:flex-1 pl-0 lg:pr-4 text-center lg:text-right'
        ):
            ui.image('/static/img/hero.png').classes(
                'w-[90%] h-auto p-4 mx-auto lg:mx-0 m-4 rounded-xl'
            )
