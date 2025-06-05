from nicegui import app, ui
from fastapi import FastAPI
import asyncio

# Import APIs
from backend.api.routes import users 

# Import routes (pages)
from frontend.routes import home
from frontend.routes import login

# Import database initializer
from backend.db.db_handler import init_db

# Create FastAPI
fastapi_app = FastAPI(title="Santipls")

# Include all routes to FastAPI
fastapi_app.include_router(users.router)
# fastapi_app.include_router(productos.router)
# fastapi_app.include_router(auth.router)

# Include FastAPI into NiceGUI
app.mount("/api", fastapi_app)

# Add static folder for frontend.
app.add_static_files('/static', 'frontend/static')

# Set home page
@ui.page('/')
def pagina_inicio():
    return home.create_home_page()

# Execute server and load app
# Set login page
@ui.page('/login')
def pagina_login():
    return login.create_login_page()

# Inicialize database when NiceGUI starts
@app.on_startup
async def startup():
    await init_db()

# Load app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080, reload=True, show=True)
