from nicegui import ui
from components.navbar import navbar  # Importa la navbar

# Página de inicio
@ui.page('/')
def home():
    navbar()  # Llama a la función navbar para incluirla
    ui.label('Bienvenido a la página de inicio').classes('text-center text-2xl')
