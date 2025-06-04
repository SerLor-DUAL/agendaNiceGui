from nicegui import ui
import requests
# Componentes
from components.navbar import navbar  
# Servicios
from services.auth_service2 import authenticateUser


# Función para manejar la página de login
@ui.page('/login')
def login():
    navbar()
    ui.label('Iniciar sesión').classes('text-center text-2xl')
    username_input = ui.input('Nombre de usuario').classes('m-2')
    password_input = ui.input('Contraseña', password=True).classes('m-2')
    
    # Botón para iniciar sesión
    ui.button('Iniciar sesión', on_click=lambda: loginUser(username_input.value, password_input.value))

def loginUser(username, password):
    # Llamamos al backend FastAPI para verificar las credenciales
    response = requests.post("http://localhost:8000/auth/login", json={"username": username, "password": password})
    ui.notify(response)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        ui.notify(f'Login exitoso! Token: {access_token}')
        ui.navigate.to('/')  # Redirige a la página principal
    else:
        ui.notify('Credenciales incorrectas')
