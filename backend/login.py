from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.authService import authenticate_user, create_access_token

router = APIRouter()

# Clase para recibir los datos del login
class LoginData(BaseModel):
    username: str
    password: str

# Ruta para realizar el login
@router.post("/login")
async def login(data: LoginData):
    user = authenticate_user(data.username, data.password)
    if user:
        # Generar token de acceso
        access_token = create_access_token(data={"sub": data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
