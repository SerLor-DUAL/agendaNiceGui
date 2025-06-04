from nicegui import ui
from services.auth_service import authenticateUser

# Función para manejar la página de login
@ui.page('/login')
def login():
    ui.label('Iniciar sesión').classes('text-center text-2xl')

    username_input = ui.input('Nombre de usuario').classes('m-2')
    password_input = ui.input('Contraseña', password=True).classes('m-2')
    
    # Botón para iniciar sesión
    ui.button('Iniciar sesión', on_click=lambda: loginUser(username_input.value, password_input.value))

def loginUser(username, password):
    if authenticateUser(username, password):
        ui.open('/home')  # Redirige a la página principal (o la página que quieras)
    else:
        ui.notify('Credenciales incorrectas')
