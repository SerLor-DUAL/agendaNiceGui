# frontend/components/diary/calendar/monthly_mode.py

# Importing necessary modules
from nicegui import ui      # Importing the ui module

def monthly_mode():
    """ Function to display the monthly mode of the calendar """
    
    # NO mostramos nada en el modo mensual
    # with ui.column().classes('w-full'):
    #     ui.label('Vista de lista mensual').classes('text-center text-gray-500 text-lg font-medium mb-4')
    #     ui.label('Los eventos se muestran en el panel lateral →').classes('text-center text-gray-400 text-sm')