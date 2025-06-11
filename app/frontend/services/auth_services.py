# app/frontend/services/auth_services.py

# Import necessary modules
import httpx                        # Importing for making HTTP requests
from typing import Optional         # Importing Optional for type hints
from dotenv import load_dotenv      # Importing load_dotenv for loading environment variables                              
import os                           # Importing os for accessing environment variables  

import aiohttp  # Usa una sesión real del navegador                                
from nicegui import ui

# Load environment variables from .env file
load_dotenv()

# Get port and base URL from environment variables and set default values
LOCALHOST_PORT = int(os.getenv("LOCALHOST_PORT", 8080))
BASE_URL = os.getenv(f"BASE_URL{LOCALHOST_PORT}", f"http://localhost:{LOCALHOST_PORT}")

# NOTE: This class handles HTTP requests for authentication with the backend
class AuthService:

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    async def login(self, nickname: str, password: str) -> dict:
            
        # JS que hará fetch con credentials para enviar la petición y que el navegador guarde cookies HttpOnly
        js_code = f"""
        fetch('{BASE_URL}/api/loginJSON', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            credentials: 'include',
            body: JSON.stringify({{ nickname: '{nickname}', password: '{password}' }})
        }})
        .then(response => {{
            if (response.ok) {{
                alert('Login correcto ✅');
                // Aquí puedes hacer más cosas tras el login, ej cargar datos o cambiar UI
            }} else {{
                alert('Error en login ❌');
            }}
        }})
        .catch(error => {{
            alert('Error de conexión: ' + error);
        }});
        """

        ui.run_javascript(js_code)
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    async def register(self, nickname: str, password: str) -> dict:
        """ Register method that sends a POST request to the backend to register a new user. """
        
        # Constructs the URL and JSON data
        url = f"{BASE_URL}/register"
        json_data = {"nickname": nickname, "password": password}
        
        # Sends the POST request
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=json_data)
                if response.status_code == 200:
                    return {"success": True, "message": "Succesful registration"}
                else:
                    return {"success": False, "message": f"Registry error: {response.text}"}
            except Exception as e:
                return {"success": False, "message": f"Connection error: {e}"}

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    async def logout(self) -> dict:
        """ Logout method that sends a POST request to the backend to logout the user. """
        
        # Constructs the URL
        url = f"{BASE_URL}/logout"
        
        # Sends the POST request
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url)
                if response.status_code == 200:
                    return {"success": True, "message": "Succesful logout"}
                else:
                    return {"success": False, "message": "Logout error"}
            except Exception as e:
                return {"success": False, "message": f"Connection error: {e}"}

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    #TODO: ADD MORE METHODS IF NEEDED

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Create an instance of the AuthService to be used in other parts of the application
front_auth_service = AuthService()
