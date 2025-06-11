# app/frontend/services/auth_services.py

# Import necessary modules
import httpx                        # Importing for making HTTP requests
from typing import Optional         # Importing Optional for type hints
from dotenv import load_dotenv      # Importing load_dotenv for loading environment variables                              
import os                           # Importing os for accessing environment variables                                  

# Load environment variables from .env file
load_dotenv()

# Get port and base URL from environment variables and set default values
LOCALHOST_PORT = int(os.getenv("LOCALHOST_PORT", 8080))
BASE_URL = os.getenv(f"BASE_URL{LOCALHOST_PORT}", f"http://127.0.0.1:{LOCALHOST_PORT}")

# NOTE: This class handles HTTP requests for authentication with the backend
class AuthService:
    
    def __init__(self):
        self.access_token: Optional[str] = None     # Initialize access token
        self.refresh_token: Optional[str] = None    # Initialize refresh token

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    async def login(self, nickname: str, password: str) -> dict:
        """ Login method that sends a POST request to the backend to authenticate the user. """
        
        # Constructs the URL and JSON data
        url = f"{BASE_URL}/api/loginJSON"
        
        json_data = {"nickname": nickname, "password": password}
        
        # Sends the POST request
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=json_data)
                
                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data.get("access_token")
                    self.refresh_token = data.get("refresh_token")
                    
                    if not self.access_token and not self.refresh_token:
                        return {"success": False, "message": "Tokens not found"}
                    
                    return {"success": True, "message": "Login successful"}
                else:
                    return {"success": False, "message": "Invalid credentials"}
                
            except Exception as e:
                return {"success": False, "message": f"Connection error: {e}"}
    
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
                    self.access_token = None
                    self.refresh_token = None
                    return {"success": True, "message": "Succesful logout"}
                else:
                    return {"success": False, "message": "Logout error"}
            except Exception as e:
                return {"success": False, "message": f"Connection error: {e}"}

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    async def get_access_token(self) -> Optional[str]:
        """ Method to get the current access token. """
        if self.access_token is None:

            url = f"{BASE_URL}/refresh"
    
    async def get_refresh_token(self) -> Optional[str]:
        """ Method to get the current refresh token. """
        return self.refresh_token
    # -------------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    
    #TODO: ADD MORE METHODS IF NEEDED

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Create an instance of the AuthService to be used in other parts of the application
front_auth_service = AuthService()
