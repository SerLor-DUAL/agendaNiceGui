from nicegui import ui
from ..components.navbar import navbar
from ..components.formCard import register_card
from ..components.headerLinks import header_links

def create_register_page():
    
    header_links()

    with ui.column().classes('w-full h-screen bg-gray-100'):
        navbar()
        register_card()
        
                