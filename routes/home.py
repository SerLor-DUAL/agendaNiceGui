from nicegui import ui
from components.navbar import navbar  # Importa la navbar
from services.session import get_user

# Página de inicio
@ui.page('/')
def home():
    navbar()  # Llama a la función navbar para incluirla
    if get_user() is None:
        #ui.navigate('/login')  # Redirige al login si no está logueado
        #return
        ui.label("No registrado")
    else:
        ui.label(f'Bienvenido, {get_user()}').classes('text-center text-2xl')

