from nicegui import ui

def navbar():
    """Crea la barra de navegación."""
    with ui.row().classes('w-full bg-blue-500 p-2 justify-between items-center'):
        # Logo (puedes poner un texto o imagen)
        ui.label('Mi Aplicación').classes('text-white text-xl')
        
        # Botones de navegación
        with ui.row().classes('gap-4'):
            ui.button('Inicio', on_click=lambda: ui.open('/home')).classes('text-white')
            ui.button('Tareas', on_click=lambda: ui.open('/tareas')).classes('text-white')
            ui.button('Perfil', on_click=lambda: ui.open('/perfil')).classes('text-white')
