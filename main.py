from nicegui import ui
#import frontend
from backend.backend import app as fastapi_app

from fastapi import FastAPI
from pydantic import BaseModel
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


# if __name__ == '__main__':
#     print('Ejecuta el servidor con el comando uvicorn main:app')
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    
