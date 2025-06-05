from nicegui import app, ui
from fastapi import FastAPI
import asyncio

# Import APIs
from backend.api.routes import users 

# Import routes (pages)
from frontend.routes import home

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

# Set home page
@ui.page('/')
def pagina_inicio():
    return home.create_home_page()

# Incialize database when NiceGUI starts
@app.on_startup
async def startup():
    await init_db()

# Execute server and load app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080, reload=True, show=True)
