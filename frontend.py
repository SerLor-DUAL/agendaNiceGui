from nicegui import ui
from fastapi import FastAPI

# NiceGUI routes
import routes.home
import routes.login

def init(fastapi_app: FastAPI) -> None:
    # Ejecuta NiceGUI con FastAPI
    ui.run_with(
        fastapi_app,
        storage_secret='mi_clave_secreta',  # Secreto para almacenamiento persistente
    )
