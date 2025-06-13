# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                             # Importing ui from nicegui
from datetime import datetime                                                      # Importing datetime for date formatting
# ----------------------------------------------------------------------------------------------------------------------------------------- #


async def create_events_card(event: dict) -> None:
    """ Creates the events page """

    # Adapt the event data to the expected format
    start = datetime.fromisoformat(event['start_date'])
    end = datetime.fromisoformat(event['end_date'])

    with ui.card().classes("w-full p-4 bg-white shadow rounded"):
        ui.label(event['title']).classes('text-xl font-semibold')
        ui.label(event['description']).classes('text-gray-700')
        ui.label(f"🕒 Desde: {start.strftime('%d %b %Y, %H:%M')}").classes('text-sm text-gray-500')
        ui.label(f"⏱️ Hasta: {end.strftime('%d %b %Y, %H:%M')}").classes('text-sm text-gray-500')
