# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                              # Importing ui from nicegui
from frontend.components.utils import navbar, header_links                          # Importing the utils components
from frontend.services.auth_services import front_auth_service as auth              # Importing the AuthService instance
from frontend.services.event_services import front_event_service as event_service   # Importing the EventService instance
from frontend.components.events.event_card import create_events_card                # Importing the event card component
# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Event simulation with mock data (Replace with actual data in the future with API or database data)
mock_events = [
    {"title": "Reunión de equipo", "description": "Planificación mensual", "date": "2025-06-15"},
    {"title": "Cita médica", "description": "Chequeo general", "date": "2025-06-20"},
    {"title": "Entrega de proyecto", "description": "Subida final al repositorio", "date": "2025-06-30"},
]

# Full authentication to access the events page
@auth.auth_required()
async def create_events_page():
    """ Creates the events page """
    
    # Get user events
    userEvents = await event_service.get_events() 
    print("User Events:", userEvents)

    # Title
    ui.label('Mis eventos').classes('text-3xl font-bold my-4')
    
    # Event cards
    with ui.column().classes('w-full gap-4'):

        if not userEvents:
            ui.label("No tienes eventos por el momento.").classes("text-gray-500")
        else:
            for event in userEvents:
                await create_events_card(event)
                
            # for event in userEvents:
            #     create_events_card(event)