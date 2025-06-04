from fastapi import FastAPI
from pydantic import BaseModel
from backend.login import login  

app = FastAPI()

# Clase para recibir los datos del login
class LoginData(BaseModel):
    username: str
    password: str

# Ruta para realizar el login
@app.post("/auth/login")
async def login_auth(data: LoginData):
    return login(data)