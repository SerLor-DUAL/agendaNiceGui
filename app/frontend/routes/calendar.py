# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                  # Importing ui from nicegui
from frontend.components.navbar import navbar                           # Importing the navbar component
from frontend.components.header_links import header_links               # Importing the header_links component
from frontend.components.diary import diary_card                        # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth  # Importing the AuthService instance

# ----------------------------------------------------------------------------------------------------------------------------------------- #


@ui.page('/calendar')
async def create_calendar_page():
    container = ui.column()  # Contenedor para UI
    
    # Label para estado inicial
    status_label = ui.label('Checking login status...', parent=container)
    
    # Esperamos a comprobar el login (no bloquea la UI)
    result = await auth.get_me()
    
    if not result.get('success', False):
        status_label.text = 'Not logged in. Redirecting...'
        # Inyecta JS para redirigir al login después de 1s
        ui.html('<script>setTimeout(() => { window.location.href="/login"; }, 1000);</script>', parent=container)
        return
    
    # Si está logueado, limpia el contenedor y crea la UI real
    container.clear()
    header_links()
    navbar()
    diary_card()