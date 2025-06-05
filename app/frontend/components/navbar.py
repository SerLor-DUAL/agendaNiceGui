from nicegui import ui

def navbar():
    from nicegui import ui

def navbar():
    with ui.row().classes(
        'items-center '     
        'justify-between '    
        'bg-gray-800 '        
        'p-4 '               
        'text-white '         
        'w-full'              
    ):
        ui.image('../static/img/logo.png').classes(
            'h-8 '    # Altura de 2rem (aprox. 32px)
            'w-auto'  # Ancho automático para conservar proporción
        )
        with ui.row().classes(
            'space-x-4' 
        ):
            # Botón de Iniciar Sesión
            ui.button('Iniciar Sesión', on_click=lambda: ui.navigate('/login')).classes(
                'bg-gray-700 '           # Fondo de gris oscuro (ligeramente más claro que el navbar)
                'hover:bg-gray-600 '     # Al pasar el ratón, el gris se aclara un poco
                'text-white '            # Texto blanco
                'px-4 '                  # Padding horizontal de 1rem (16px)
                'py-2 '                  # Padding vertical de 0.5rem (8px)
                'rounded'                # Bordes redondeados
            )

            # Botón de Registro
            ui.button('Registro', on_click=lambda: ui.navigate('/register')).classes(
                'bg-blue-500 '           # Fondo azul medio
                'hover:bg-blue-400 '     # Al pasar el ratón, el azul se hace más claro
                'text-white '            # Texto blanco
                'px-4 '                  # Padding horizontal de 1rem (16px)
                'py-2 '                  # Padding vertical de 0.5rem (8px)
                'rounded'                # Bordes redondeados
            )
