# Import necessary modules
import httpx                        # Importing for making HTTP requests
from dotenv import load_dotenv      # Importing load_dotenv for loading environment variables   
import os                           # Importing os for environment variable handling                           
from nicegui import ui              # Importing ui from nicegui

from collections import defaultdict
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get port and base URL from environment variables and set default values
LOCALHOST_PORT = int(os.getenv("LOCALHOST_PORT", 8080))
BASE_URL = os.getenv(f"BASE_URL{LOCALHOST_PORT}", f"http://localhost:{LOCALHOST_PORT}")

# NOTE: The following code is a service for handling events, it is not a route.
class EventService:
    """ Service for handling events """
    
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=BASE_URL)  # Initialize the HTTP client with the base URL

# -------------------------------------------------------------------------------------------------------------------------------------
# CRUD CALLS TO THE API
# READ
    async def get_events(self):
        """ Get all events """
        js_code = f'''
        fetch('{BASE_URL}/api/events', {{
            method: 'GET',
            credentials: 'include'
        }})
        .then(response => {{
            if (!response.ok) throw new Error(`Error ${{response.status}}: ${{response.statusText}}`);
            return response.json();
        }})
    '''
        # Execute fetch from the browser
        try:
            # Execute the JS, wait for the response, and parse the JSON
            events = await ui.run_javascript(js_code, timeout=5)
            print(events)
            if isinstance(events, dict) and events.get('error'):
                ui.notify(f"Error obteniendo los eventos: {events['error']}", color='negative')
                return None
            group_events = self.group_events_by_date(events)
            return group_events

        except Exception as e:
                ui.notify(f"Error ejecutando el fetch: {str(e)}", color='negative')
                return None

# -------------------------------------------------------------------------------------------------------------------------------------
# CREATE
    async def create_event(self, event_data: dict):
        """ Create a new event by sending a POST request via browser fetch """
        js_code = f'''
        fetch('{BASE_URL}/api/events', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            credentials: 'include',
            body: JSON.stringify({{
                "title": "{event_data['title']}",
                "description": "{event_data['description']}",
                "start_date": "{event_data['start_date']}",
                "end_date": "{event_data['end_date']}"
            }})
        }})
        .then(response => {{
            if (!response.ok) throw new Error(`Error ${{response.status}}: ${{response.statusText}}`);
            return response.json();
        }})
        '''

        try:
            result = await ui.run_javascript(js_code, timeout=5)
            print('Evento creado:', result)
            ui.notify('Evento creado con éxito', color='positive')
            return result
        except Exception as e:
            print('Error al crear evento:', e)
            ui.notify(f'Error creando evento: {str(e)}', color='negative')
            return None
        
# -------------------------------------------------------------------------------------------------------------------------------------
# DELETE
    async def delete_event(self, event_id: int):
        """ Delete an event by ID using a browser-side fetch call """
        js_code = f'''
        fetch('{BASE_URL}/api/events/{event_id}', {{
            method: 'DELETE',
            credentials: 'include'
        }})
        .then(response => {{
            if (!response.ok) throw new Error(`Error ${{response.status}}: ${{response.statusText}}`);
            return response.json();
        }})
        '''

        try:
            result = await ui.run_javascript(js_code, timeout=5)
            print('Evento eliminado:', result)
            return True
        except Exception as e:
            print('Error al eliminar evento:', e)
            return False

# -------------------------------------------------------------------------------------------------------------------------------------
# UPDATE
    async def update_event(self, event_id: int, updated_data: dict):
        """ Update an event by ID using a browser-side fetch call """
        js_code = f'''
        fetch('{BASE_URL}/api/events/{event_id}', {{
            method: 'PUT',
            credentials: 'include',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({updated_data})
        }})
        .then(response => {{
            if (!response.ok) throw new Error(`Error ${{response.status}}: ${{response.statusText}}`);
            return response.json();
        }})
        '''

        try:
            result = await ui.run_javascript(js_code, timeout=5)
            print('Evento actualizado:', result)
            ui.notify('Evento actualizado correctamente', color='positive')
            return result
        except Exception as e:
            print('Error al actualizar evento:', e)
            ui.notify(f'Error actualizando evento: {str(e)}', color='negative')
            return None

    
    @staticmethod
    def group_events_by_date(events: list) -> dict:
        event_group = defaultdict(list)
        for event in events:
            try:
                date = datetime.fromisoformat(event['start_date']).strftime('%d/%m/%Y')
                event_group[date].append(event)
            except Exception as e:
                print(f"Error procesando evento: {event}, {e}")
        return dict(event_group)
        

# Create an instance of the EventService
front_event_service = EventService()  # Create an instance of the EventService