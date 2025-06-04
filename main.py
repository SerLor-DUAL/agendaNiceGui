from nicegui import app, ui
from fastapi import FastAPI

# Import APIs
from app.backend.api.routes import users 

# Import routes (pages)
from app.frontend.routes import home

# Create FastAPI
fastapi_app = FastAPI(title="Santipls")

# Include all routes to FastAPI
fastapi_app.include_router(users.router, prefix="/api")
# fastapi_app.include_router(productos.router, prefix="/api")
# fastapi_app.include_router(auth.router, prefix="/api")

# Include into NiceGUI FastAPI
app.mount("/api", fastapi_app)

# Set jome page
@ui.page('/')
def pagina_inicio():
    return home.create_home_page()

# Load app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080, reload=True, show=True)
