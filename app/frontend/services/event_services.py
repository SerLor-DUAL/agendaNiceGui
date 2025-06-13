# Import necessary modules
import httpx                        # Importing for making HTTP requests
from dotenv import load_dotenv      # Importing load_dotenv for loading environment variables   
import os                           # Importing os for environment variable handling                           
from nicegui import ui              # Importing ui from nicegui

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

    async def get_events(self, *args, **kwargs):
        """ Get all events """
        url = f"{BASE_URL}/api/events"
        try:
            response = await self.client.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                ui.notify(f"Error al obtener los eventos: {response.status_code} - {response.text}", color='negative')
                return None
        except Exception as e:
            ui.notify(f"Error al obtener los eventos: {str(e)}", color='negative')
            return None

    async def create_event(self, event_data):
        """ Create a new event """
        

    async def delete_event(self, event_id):
        """ Delete an event by ID """
        

# Create an instance of the EventService
front_event_service = EventService()  # Create an instance of the EventService