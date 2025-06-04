import frontend
from fastapi import FastAPI
from backend.login import router as login_router  # Importa el router de backend
from nicegui import ui


app = FastAPI()

# Registra el router de login
app.include_router(login_router, prefix="/auth", tags=["auth"])

# Inicializa NiceGUI
frontend.init(app)

if __name__ == '__main__':
    print('Ejecuta el servidor con el comando uvicorn main:app')
    # import uvicorn
    # uvicorn.run(app, host="localhost", port=8000)
    ui.run()
    
