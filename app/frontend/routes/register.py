from nicegui import ui
from ..components.navbar import navbar
from ..components.formCard import register_card

def create_register_page():
    # Agrega aquí el CSS personalizado
    ui.add_head_html('<link rel="stylesheet" href="/static/css/styleColores.css">')
    
    with ui.column().classes('w-full h-screen bg-gray-100'):
        navbar()
        register_card()
        
                