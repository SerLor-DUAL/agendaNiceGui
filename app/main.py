from nicegui import app, ui
from fastapi import FastAPI

# Import APIs
from backend.api.routes import users 
from backend.api.routes import auth 
from backend.api.routes import events

# Import routes (pages)
from frontend.routes import home
from frontend.routes import login
from frontend.routes import register
from frontend.routes import calendar

# Import database initializer
from backend.db.db_handler import init_db

# Import modules to load and access environment variables
from dotenv import load_dotenv                                
import os                                                     

# Load environment variables from .env file
load_dotenv()

# ============================================================================================================================= #
#                                           FastAPI and NiceGUI initial integration                                             #
# ============================================================================================================================= #

# Create FastAPI instance
fastapi_app = FastAPI(title="Integra")

# Include all the needed routes to FastAPI
fastapi_app.include_router(users.userRouter)      # Users API
fastapi_app.include_router(auth.authRouter)       # Authentication API
fastapi_app.include_router(events.event_router)  # Events API
# Include FastAPI into NiceGUI
app.mount("/api", fastapi_app)

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

# ============================================================================================================================= #
#                                           Pages configuration                                                                 #
# ============================================================================================================================= #

# Set home page
@ui.page('/')
def pagina_inicio():
    return home.create_home_page()

# Set login page
@ui.page('/login')
def pagina_login():
    return login.create_login_page()

# Set register page
@ui.page('/register')
def pagina_register():
    return register.create_register_page()

# Set calendar page
@ui.page('/calendar')  
def pagina_calendar():
    return calendar.create_calendar_page()

# ============================================================================================================================= #
#                                           Database and app initialization                                                     #
# ============================================================================================================================= #

# Inicialize database when NiceGUI starts
@app.on_startup
async def startup():
    await init_db()

# Load app
if __name__ in {"__main__", "__mp_main__"}:
    
    selected_port = int(os.getenv("LOCALHOST_PORT", 8000))  # Get port from environment variable, if not set, default to 8000
    
    # Runs app
    ui.run(port=selected_port, reload=True, show=True)
