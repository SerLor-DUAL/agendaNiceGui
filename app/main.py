from nicegui import app, ui
from fastapi import FastAPI
import os

# Import APIs
from backend.api.routes import users 
from backend.api.routes import auth 

# Import routes (pages)
from frontend.routes import home
from frontend.routes import login
from frontend.routes import register

# Import database initializer
from backend.db.db_handler import init_db

# ============================================================================================================================= #
#                                           FastAPI and NiceGUI initial integration                                             #
# ============================================================================================================================= #

# Create FastAPI instance
fastapi_app = FastAPI(title="Integra")

# Include all the needed routes to FastAPI
fastapi_app.include_router(users.userRouter)      # Users API
fastapi_app.include_router(auth.authRouter)       # Authentication API

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

# ============================================================================================================================= #
#                                           Database and app initialization                                                     #
# ============================================================================================================================= #

# Inicialize database when NiceGUI starts
@app.on_startup
async def startup():
    await init_db()

# Load app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8081, reload=True, show=True)
