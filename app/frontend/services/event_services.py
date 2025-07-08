# frontend/services/event_services.py

# Import necessary modules
import httpx                            # Importing for making HTTP requests
from dotenv import load_dotenv          # Importing load_dotenv for loading environment variables   
import os                               # Importing os for environment variable handling                           
from nicegui import ui                  # Importing ui from nicegui
from collections import defaultdict     # Importing defaultdict for grouping events by date
from datetime import datetime           # Importing datetime for date handling

# Load environment variables from .env file
load_dotenv()

# Get port and base URL from environment variables and set default values
LOCALHOST_PORT = int(os.getenv("LOCALHOST_PORT", 8080))
BASE_URL = os.getenv(f"BASE_URL{LOCALHOST_PORT}", f"http://localhost:{LOCALHOST_PORT}")

# NOTE: The following code is a service for handling events.
class EventService:
    
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=BASE_URL)  # Initialize the HTTP client with the base URL

    # ------------------------------------------------------------------------------------------------------------------------------------- #
    # READ
    
    async def get_events(self):
        """ Get all events """
        
        # JavaScript code to fetch events from the backend API
        js_code = f'''
                        fetch('{BASE_URL}/api/events', {{
                            method: 'GET',
                            credentials: 'include'
                        }})
                        .then(response => {{
                            if (response.status === 404) {{
                                return {{notFound: true}};
                            }}
                            if (!response.ok) throw new Error(`Error ${{response.status}}: ${{response.statusText}}`);
                            return response.json();
                        }})
                    '''
                    
        # Execute fetch from the browser
        try:
            # Execute the JS, wait for the response, and parse the JSON
            events = await ui.run_javascript(js_code, timeout=7)
            
            # Si la respuesta es notFound, muestra aviso y retorna un dict vacío
            if isinstance(events, dict) and events.get('notFound'):
                # Por el momento no se muestra un aviso, pero podriamos descomentar si se desea
                # ui.notify("No se encontraron eventos", color='warning')
                return {}
            
            # Check if the response is an error
            if isinstance(events, dict) and events.get('error'):
                ui.notify(f"Error obteniendo los eventos: {events['error']}", color='negative')
                return None
            
            # If the response is valid, group the events by date
            group_events = self.group_events_by_date(events)
            
            return group_events

        # If there's an error executing the fetch, notify the user
        except Exception as e:
                ui.notify(f"Error ejecutando el fetch: {str(e)}", color='negative')
                return None

    # ------------------------------------------------------------------------------------------------------------------------------------- #
    # CREATE
    
    async def create_event(self, event_data: dict):
        """ Creates a new event by sending a POST request via browser fetch """
        
        # Javascript code to create an event using the fetch API
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
            # Execute the JS code to create the event
            result = await ui.run_javascript(js_code, timeout=5)
            
            # Print the result for debugging
            print('Created event:', result)
            
            return result
        
        # If there's an error executing the fetch, notify the user
        except Exception as e:
            print('Error al crear evento:', e)
            ui.notify(f'Error creando evento: {str(e)}', color='negative')
            return None
        
    # ------------------------------------------------------------------------------------------------------------------------------------- #
    # DELETE

    async def delete_event(self, event_id: int):
        """ Delete an event by ID using a browser-side fetch call """
        
        # JavaScript code to delete an event using the fetch API
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
            # Execute the JS code to delete the event
            result = await ui.run_javascript(js_code, timeout=5)
            
            # Print the result for debugging
            print('Deleted event:', 'Deleted' if result else 'Not Deleted')
            if result:
                print('Deleted id:', event_id)
                
            return True
        
        # If there's an error executing the fetch, notify the user
        except Exception as e:
            print('Error al eliminar evento:', e)
            return False

    # ------------------------------------------------------------------------------------------------------------------------------------- #
    # UPDATE
    
    async def update_event(self, event_id: int, updated_data: dict):
        """ Update an event by ID using a browser-side fetch call """
        
        # JavaScript code to update an event using the fetch API
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
            # Execute the JS code to update the event
            result = await ui.run_javascript(js_code, timeout=5)
            
            # Print the result for debugging
            print('Updated event:', result)
            
            return result
        except Exception as e:
            print('Error al actualizar evento:', e)
            ui.notify(f'Error actualizando evento: {str(e)}', color='negative')
            return None

    # ------------------------------------------------------------------------------------------------------------------------------------- #
    # AUXILIARY

    @staticmethod
    def group_events_by_date(events: list) -> dict:
        """ Group events by their start date """
        
        # Create a defaultdict to group events by date
        event_group = defaultdict(list)
        
        # Iterate through the events and group them by date
        for event in events:
            try:
                date = datetime.fromisoformat(event['start_date']).strftime('%d/%m/%Y')
                event_group[date].append(event)
            except Exception as e:
                print(f"Error procesando evento: {event}, {e}")
        return dict(event_group)
        
        
# ------------------------------------------------------------------------------------------------------------------------------------- #

# CreateS a global instance of the EventService
front_event_service = EventService() 