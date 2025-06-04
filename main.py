from nicegui import ui
from fastapi import FastAPI
from pydantic import BaseModel
# Backend imports
from backend.login import login  
# NiceGUI routes
import routes.home
import routes.login

app = FastAPI()

# Clase para recibir los datos del login
class LoginData(BaseModel):
    username: str
    password: str

# Ruta para realizar el login
@app.post("/auth/login")
async def login_auth(data: LoginData):
    return login(app, data)

# Inicializa NiceGUI
ui.run()


