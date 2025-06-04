from nicegui import ui
from components.navbar import navbar  # Importa la navbar
from services.session import getUser

# Página de inicio
@ui.page('/')
def home():
    navbar()  # Llama a la función navbar para incluirla
    #if getUser() is None:
    #    ui.navigate.to('/login')  # Redirige al login si no está logueado
    #    return
    ui.label(f'Bienvenido, {getUser()}').classes('text-center text-2xl')

