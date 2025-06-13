# components/diary/diary_day_card.py

# Import necessary modules
from nicegui import ui  # Import the ui module

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to create a calendar day card
def create_diary_day_card(day: int):
    """ Function to create a calendar day card """
    
    with ui.card().style('min-height: 80px; border: 1px solid #eee; background-color: #fff;'):
        
        if day > 0:
            
            # Create a label with the day number
            ui.label(str(day)).classes('text-sm font-medium')
            
            with ui.menu().classes("relative"):
                ui.menu_item('Añadir evento', on_click=lambda: ui.notify(f'Añadir evento al día {day}'))
                ui.menu_item('Ver tareas', on_click=lambda: ui.notify(f'Tareas para el día {day}'))
            
        else:
            
            # Create an empty label
            ui.label("").classes('text-sm')
