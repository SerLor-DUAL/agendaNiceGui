from nicegui import app, ui
from fastapi import FastAPI

# Import CORS middleware to handle cross-origin requests
from backend.utils.cors import setup_cors

# Import APIs endopints
from backend.api.routes import events, events_admin, users_admin, auth

# Import routes (pages)
from frontend.routes import home, login, register, diary

# Import database initializer
from backend.db.db_handler import init_db

# Import modules to load and access environment variables
from dotenv import load_dotenv                                
import os                                                     

# Load environment variables from .env file
load_dotenv()

# Import added custom links to head in the HTML
from frontend.components.utils.header_links import header_links

# Import principal page components
from frontend.components.utils import navbar

from frontend.services.auth_services import front_auth_service, with_first_init

# ============================================================================================================================= #
#                                           FastAPI and NiceGUI initial integration                                             #
# ============================================================================================================================= #

# Create FastAPI instance
fastapi_app = FastAPI(title="Integra")

# Injects CORS middleware into the FastApi instance
setup_cors(fastapi_app)

# Include all the needed routes to FastAPI
fastapi_app.include_router(users_admin.user_admin_router)       # Administration of users API
fastapi_app.include_router(auth.auth_router)                    # Authentication API
fastapi_app.include_router(events.event_router)                 # Events API
fastapi_app.include_router(events_admin.event_admin_router)     # Administration of events API

# Include FastAPI into NiceGUI
app.mount("/api", fastapi_app)
app.storage.max_tab_storage_age = 1
# ============================================================================================================================= #
#                                           Directory configuration                                                             #
# ============================================================================================================================= #

# Configuration of base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Definition of the path to the static files
STATIC_PATH = os.path.join(BASE_DIR, 'frontend', 'static')
if not os.path.isdir(STATIC_PATH):
    raise FileNotFoundError(f"No se encontró la carpeta estática: {STATIC_PATH}")   # Check if the static folder exists

# ============================================================================================================================= #

# Add static folder for frontend.
app.add_static_files('/static', STATIC_PATH)

# Add customs CSS to the head
header_links()

# ============================================================================================================================= #
#                                           Pages configuration                                                                 #
# ============================================================================================================================= #

# =====================#
#     Global pages     #
# =====================#

# Set home page
@ui.page('/')
@with_first_init(front_auth_service)
async def page_init():
    await navbar()
    await home.create_home_page()

# Set login page
@ui.page('/login')
@with_first_init(front_auth_service)
async def page_login():
    await navbar()
    await login.create_login_page()

# Set register page
@ui.page('/register')
@with_first_init(front_auth_service)
async def page_register():
    await navbar()
    await register.create_register_page()

# =====================#
#  Authorizated pages  #
# =====================#

# Set calendar page
@ui.page('/diary')  
async def page_diary():
    await navbar()
    await diary.create_diary_page()

# ============================================================================================================================= #
#                                           Database and app initialization                                                     #
# ============================================================================================================================= #

# Inicialize database when NiceGUI starts
@app.on_startup
async def startup():
    await init_db()

# Load app
if __name__ in {"__main__", "__mp_main__"}:
    
    # Get port from environment variable, if not set, default to 8000
    selected_port = int(os.getenv("LOCALHOST_PORT", 8000))  
    
    # Get JWT secret key from environment variable
    jwt_secret_key = os.getenv("JWT_SECRET_KEY")
    
    # Runs app
    ui.run(port=selected_port, reload=True, show=True, storage_secret=jwt_secret_key, tailwind=True)
