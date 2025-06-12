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
            
            # NOTE here you can add more details about the day, like events or tasks
            # For example a icon or label for events
            
        else:
            
            # Create an empty label
            ui.label("").classes('text-sm')
