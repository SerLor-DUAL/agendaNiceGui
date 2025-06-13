# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                             # Importing ui from nicegui
from datetime import datetime                                                      # Importing datetime for date formatting
# ----------------------------------------------------------------------------------------------------------------------------------------- #


async def create_events_card(event: dict) -> None:
    """ Creates the events page """
    with ui.card().classes("w-full p-4 bg-white shadow rounded"):
        ui.label(event['title']).classes('text-xl font-semibold')
        ui.label(event['description']).classes('text-gray-700')
        #ui.label(f"📅 {datetime.strptime(event['start_date'], '%Y-%m-%d').strftime('%d %b %Y')}").classes('text-sm text-gray-500')
        #ui.label(f"📅 {datetime.strptime(event['end_date'], '%Y-%m-%d').strftime('%d %b %Y')}").classes('text-sm text-gray-500')
    # userEvents = event_service.get_events() 