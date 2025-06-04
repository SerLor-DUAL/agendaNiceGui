from nicegui import ui, app
# Componentes
from components.navbar import navbar  
# Servicios
from services.authService import authenticate_user, create_access_token


@ui.page('/login')
def login():
    ui.label('Iniciar sesión').classes('text-center text-2xl')
    username_input = ui.input('Nombre de usuario').classes('m-2')
    password_input = ui.input('Contraseña', password=True).classes('m-2')

    def loginUser():
        username = username_input.value.strip()
        password = password_input.value.strip()
        user = authenticate_user(username, password)
        if user:
            token = create_access_token({"sub": user["username"]})
            app.storage.user.update({'username': user["username"], 'token':token, 'authenticated': True})
            ui.notify('¡Inicio de sesión exitoso!')
            ui.navigate.to('/')
        else:
            ui.notify('Credenciales incorrectas', type='negative')
    
    ui.button('Iniciar sesión', on_click=loginUser)
