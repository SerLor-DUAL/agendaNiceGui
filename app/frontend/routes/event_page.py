# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                  # Importing ui from nicegui
from frontend.components.utils import navbar, header_links              # Importing the utils components
from frontend.components.diary import diary_card                        # Importing the calendar_card component
from frontend.services.auth_services import front_auth_service as auth  # Importing the AuthService instance
from frontend.services.event_services import front_event_service as event_service  # Importing the EventService instance
from datetime import datetime  # Importing datetime for date formatting
# ----------------------------------------------------------------------------------------------------------------------------------------- #
# Simulación de eventos (esto luego vendría de una base de datos o API)
mock_events = [
    {"title": "Reunión de equipo", "description": "Planificación mensual", "date": "2025-06-15"},
    {"title": "Cita médica", "description": "Chequeo general", "date": "2025-06-20"},
    {"title": "Entrega de proyecto", "description": "Subida final al repositorio", "date": "2025-06-30"},
]


@auth.auth_required()
async def create_events_page():
    """ Creates the events page """
    # Build UI
    header_links()
    navbar()
    ui.label('Mis eventos').classes('text-3xl font-bold my-4')
    with ui.column().classes('w-full gap-4'):

        if not mock_events:
            ui.label("No tienes eventos por el momento.").classes("text-gray-500")
        else:
            for event in mock_events:
                with ui.card().classes("w-full p-4 bg-white shadow rounded"):
                    ui.label(event['title']).classes('text-xl font-semibold')
                    ui.label(event['description']).classes('text-gray-700')
                    ui.label(f"📅 {datetime.strptime(event['date'], '%Y-%m-%d').strftime('%d %b %Y')}").classes('text-sm text-gray-500')
    # userEvents = event_service.get_events() 