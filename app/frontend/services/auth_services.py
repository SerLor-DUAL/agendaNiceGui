# app/frontend/services/auth_services.py

# Import necessary modules
import time                                                                 # Importing time to caculate localstorage purge
import httpx                                                                # Importing for making HTTP requests
from dotenv import load_dotenv                                              # Importing load_dotenv for loading environment variables                              
import os                                                                   # Importing os for accessing environment variables  
from nicegui import ui, app                                                 # Importing ui and app from nicegui
from functools import wraps                                                 # Importing wraps for decorator usage
from frontend.utils.routing import front_router_handler as frh              # Importing the RouteHandler   

# Load environment variables from .env file
load_dotenv()

# Get port and base URL from environment variables and set default values
LOCALHOST_PORT = int(os.getenv("LOCALHOST_PORT", 8080))
BASE_URL = os.getenv(f"BASE_URL{LOCALHOST_PORT}", f"http://localhost:{LOCALHOST_PORT}")

# NOTE: This class handles HTTP requests for authentication with the backend
        # To obtain the cookies in the client, a JavaScript fetching method is used, this is used in the login and refresh token methods
        # To check the cookies in the client, a JavaScript fetching method is used, this is used in the get_me method
class AuthService:

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # COOKIES DEPENDANT METHODS #
    
    async def get_me(self) -> dict:
        """ Validates user authentication and retrieves profile data using HttpOnly cookies.
            
            Uses JavaScript fetch to securely send browser cookies to the backend's '/api/me-cookie'
            endpoint. This is the recommended method for HttpOnly cookie authentication as it prevents
            client-side token exposure while maintaining session security. """
        
        js_code = f"""
                        return fetch('{BASE_URL}/api/me-cookie', {{
                            method: 'GET',
                            credentials: 'include'
                        }})
                        .then(response => {{
                            if (!response.ok) throw new Error('Unauthorized or error');
                            return response.json();
                        }})
                        .then(data => {{
                            return {{ success: true, data: data }};
                        }})
                        .catch(error => {{
                            return {{ success: false, message: error.message }};
                        }});
                    """
        result = await ui.run_javascript(js_code, timeout=10)
        return result


    async def login(self, nickname: str, password: str, success_message: str = "Inicio de sesión con exito") -> dict:
        """ Login method that sends a POST request to the backend to login the user. It obtains cookies for the browser using a JavaScript fetch. """
        
        # JavaScript code to send the login request
        js_code = f"""
                        return fetch('{BASE_URL}/api/loginJSON', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            credentials: 'include',
                            body: JSON.stringify({{ nickname: '{nickname}', password: '{password}' }})
                        }})
                        .then(async response => {{
                            if (response.ok) {{
                                const data = await response.json();
                                return {{
                                    status: 'success',
                                    code: response.status,
                                    message: '{success_message}',
                                }};
                            }} else {{
                                const errorData = await response.json().catch(() => ({{}}));
                                return {{
                                    status: 'error',
                                    code: response.status,
                                    message: errorData.detail || 'Unknown error'
                                }};
                            }}
                        }})
                        .catch(error => {{
                            return {{
                                status: 'error',
                                message: error.toString()
                            }};
                        }});
                    """

        # Runs the JavaScript code
        result = await ui.run_javascript(js_code, timeout=5.0)

        # After geting a result we load the session again. With these, every component that used
        # the app.storage.user will have it reloaded to use it.
        await self.load_user_session()
        # Returns a response from the fetched JavaScript code
        return result


    async def logout(self) -> dict:
        """ Logout method that sends a POST request to the backend to logout the user. It may obtain/update cookies for the browser using a JavaScript fetch. """
        
        js_code = f"""
                        return fetch('{BASE_URL}/api/logout', {{
                            method: 'POST',
                            credentials: 'include',
                        }})
                        .then(async response => {{
                            if (response.ok) {{
                                const data = await response.json().catch(() => ({{}}));
                                return {{
                                    status: 'success',
                                    code: response.status,
                                    message: 'Token refreshed',
                                }};
                            }} else {{
                                const errorData = await response.json().catch(() => ({{}}));
                                return {{
                                    status: 'error',
                                    code: response.status,
                                    message: errorData.detail || 'Failed to refresh token'
                                }};
                            }}
                        }})
                        .catch(error => {{
                            return {{
                                status: 'error',
                                message: error.toString()
                            }};
                        }});
                    """
                    
        # Runs the JavaScript code
        result = await ui.run_javascript(js_code, timeout=10.0)
        
        # Returns a response from the fetched JavaScript code
        if result and result.get('status') == 'success':
            # Clears the local cache
            app.storage.user.clear()
            frh.go_to('/')
            return {"success": True, "message": result.get('message')}
        else:
            return {"success": False, "message": result.get('message')}


    async def refresh_token(self) -> dict:
        """ Refresh token method that sends a POST request to the backend to refresh the user's token. It may obtain/update cookies for the browser using a JavaScript fetch. """
        
        js_code = f"""
                        return fetch('{BASE_URL}/api/refresh-token', {{
                            method: 'POST',
                            credentials: 'include',
                        }})
                        .then(async response => {{
                            if (response.ok) {{
                                const data = await response.json().catch(() => ({{}}));
                                return {{
                                    status: 'success',
                                    code: response.status,
                                    message: 'Token refreshed',
                                }};
                            }} else {{
                                const errorData = await response.json().catch(() => ({{}}));
                                return {{
                                    status: 'error',
                                    code: response.status,
                                    message: errorData.detail || 'Failed to refresh token'
                                }};
                            }}
                        }})
                        .catch(error => {{
                            return {{
                                status: 'error',
                                message: error.toString()
                            }};
                        }});
                    """
                    
        # Runs the JavaScript code
        result = await ui.run_javascript(js_code, timeout=5.0)
        
        # Returns a response from the fetched JavaScript code
        return result
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    async def register(self, nickname: str, password: str) -> dict:
        """ Register method that sends a POST request to the backend to register a new user. """
        
        # Constructs the URL and JSON data
        url = f"{BASE_URL}/api/register"
        json_data = {"nickname": nickname, "password": password}
        
        # Sends the POST request
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=json_data)
                if response.status_code == 200:
                    
                    # If the registration is successful, login the user to obtain the cookies for the browser
                    login_result = await self.login(nickname, password, success_message="Successful registration")
                    return login_result
                else:
                    return {"success": False, "message": f"Error de registro: {response.text}"}
            except Exception as e:
                return {"success": False, "message": f"Error de conexión: {e}"}

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # NOTE: This method will be used as a decorator or as a boolean checker to check if the user is logged in
    def auth_required(self, check_only: bool = False):
        """ Function to be used as a decorator or as a boolean checker to check if the user is logged in """

        async def check_auth():
             
            #  First check local cache
            if 'user_id' in app.storage.user:
                return True
            
            # If there is no user data in the local cache, load the user session
            return await self.load_user_session()

        # Boolean mode
        if check_only:
            return check_auth()

        # Decorator mode
        def decorator(function):
            
            # Wrapper function
            @wraps(function)
            async def wrapper(*args, **kwargs):

                # Show loading dialog
                with ui.dialog() as dialog, ui.card():
                    ui.label('Checking session...')
                    ui.spinner()
                    
                dialog.open()

                # Checks the authentication
                is_authenticated = await check_auth()
                
                # If the user is not logged in, redirects to the login page
                if not is_authenticated:
                    ui.notify('You are not logged in. Redirecting to login...', color='negative')
                    frh.go_to('/login')
                else:
                    # If the user is logged in, executes the original function
                    dialog.close()
                    return await function(*args, **kwargs)
            
            # Returns the wrapper function            
            return wrapper
        
        # Returns the decorator
        return decorator
    
    
    async def load_user_session(self) -> bool:
        """ Loads the user session from the backend cookies and stores the user data in app.storage.user, 
            returns True if the session is valid, False if not. """
        # Checks if the user is logged in
        result = await self.get_me()
        
        if result.get('success'):
            user_data = result.get('data', {})
            
            # Save the user data in app.storage.user
            app.storage.user['user_id'] = user_data.get('id')
            app.storage.user['nickname'] = user_data.get('nickname')
            # Add timestamp to know when to delete the session
            app.storage.user['ts'] = time.time()
            return True
        else:
            return False
# ----------------------------------------------------------------------------------------------------------------------------------------------------    
    # FIRST INIT. It will be used as a decorator.
    async def first_init(self) -> None:
        """During the first INIT we will try to set up the user."""
        # Validate the session: if no tokens are present and the session has expired, clear the local storage.
        is_session_valid()
        if not app.storage.user.get('session_initialized', False):
            await self.load_user_session()
        app.storage.user['session_initialized'] = True


      
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

#TODO: ADD MORE METHODS IF NEEDED

# Create an instance of the AuthService to be used in other parts of the application
front_auth_service = AuthService()

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# FIRST INIT DECORATOR.
def with_first_init(auth_service_instance):
    def decorator(view_function):
        @wraps(view_function)
        async def wrapper(*args, **kwargs):
            await auth_service_instance.first_init()
            return await view_function(*args, **kwargs)
        return wrapper
    return decorator

# SESSION VALID
@staticmethod
def is_session_valid(max_age: int = 86400) -> bool:
    ts = app.storage.user.get('ts')
    if not ts:
        return False
    if time.time() - ts > max_age:
        app.storage.user.clear()
        return False
    return True

