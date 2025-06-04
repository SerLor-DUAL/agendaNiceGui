from nicegui import ui

def create_home_page():
    with ui.column().classes('w-full items-center p-8'):
        ui.html('<h1>🏠 Bienvenido a Mi App</h1>').classes('text-4xl font-bold mb-8')
        
        with ui.card().classes('w-96 p-6'):
            ui.label('¿Qué quieres hacer?').classes('text-xl mb-4')
            
            with ui.column().classes('w-full gap-4'):
                ui.button('👥 Ver Usuarios', 
                    on_click=lambda: ui.navigate.to('/usuarios')
                ).classes('w-full').props('size=large color=primary')
                
                ui.button('🔐 Iniciar Sesión', 
                    on_click=lambda: ui.navigate.to('/login')
                ).classes('w-full').props('size=large color=secondary')