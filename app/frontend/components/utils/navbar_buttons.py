# frontend/components/navbar_buttons.py

# Import necesary modules
from nicegui import ui                                                      # Import the ui module
from frontend.services.auth_services import front_auth_service as auth      # Importing the AuthService instance
from frontend.utils.routing import front_router_handler as frh              # Importing the RouteHandler

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Styles for the desktop buttons
desktop_button_classes = (
                            'flex items-center gap-2 '
                            'bg-blue-600 hover:bg-blue-500 active:bg-blue-700 '
                            'text-white font-semibold '
                            'px-4 py-2 rounded-lg '
                            'transition-colors duration-200 '
                            'whitespace-nowrap'
                        )

# Styles for mobile buttons  
mobile_button_classes = (
                            'bg-blue-600 hover:bg-blue-500 '
                            'text-white px-4 py-3 rounded-lg '
                            'w-full text-left transition-colors duration-200'
                        )
            
# NOTE: Function to add the navbar buttons component for desktop
async def navbar_buttons():
    logged = await auth.auth_required(check_only=True)

    # If user is logged in show logout button, if not show login and register buttons
    if logged:
        ui.button('Cerrar Sesión', on_click=lambda: auth.logout()).classes(desktop_button_classes)
    else:
        ui.button('Iniciar Sesión', on_click=lambda: frh.go_to('/login')).classes(desktop_button_classes)
        ui.button('Registro', on_click=lambda: frh.go_to('/register')).classes(desktop_button_classes)

# NOTE: Function to add the navbar buttons component for mobile
async def mobile_nav_buttons():
    logged = await auth.auth_required(check_only=True)

    # If user is logged in show logout button, if not show login and register buttons
    with ui.column().classes('space-y-2 w-full'):
        if logged:
            ui.button('Cerrar Sesión', on_click=lambda: auth.logout()).classes(mobile_button_classes)
        else:
            ui.button('Iniciar Sesión', on_click=lambda: frh.go_to('/login')).classes(mobile_button_classes)
            ui.button('Registro', on_click=lambda: frh.go_to('/register')).classes(mobile_button_classes)