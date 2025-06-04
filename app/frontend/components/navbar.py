from nicegui import ui

def navbar():
    with ui.row().classes('items-center justify-between bg-blue-600 p-4 text-white w-full'):
        ui.label('Mi Aplicación').classes('text-2xl font-bold')  # Título de la aplicación
        with ui.row():
            ui.button('Inicio', on_click=lambda: ui.navigate('/home')).classes('text-white hover:bg-blue-500 mx-2')
            ui.button('Acerca de', on_click=lambda: ui.navigate('/about')).classes('text-white hover:bg-blue-500 mx-2')
            ui.button('Contacto', on_click=lambda: ui.navigate('/contact')).classes('text-white hover:bg-blue-500 mx-2')