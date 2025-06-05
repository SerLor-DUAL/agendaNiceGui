from nicegui import ui
from ..components.navbar import navbar

def create_login_page():
    navbar()
from nicegui import ui
from frontend.components.navbar import navbar

def create_login_page():
    with ui.column().classes('w-full h-screen bg-gray-100'):
        navbar()
        # Container that takes the full height of the screen (h-screen) and centers its content
        with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
            # Login card
            with ui.card().classes('bg-white p-8 rounded-lg shadow-lg max-w-md w-6/7 sm:w-full '):
                ui.markdown('# Iniciar Sesión').classes(
                'text-xs sm:text-2xl font-bold text-[#1F2937] mb-6 text-center'
                )   
                # User
                username_input = ui.input(
                    'Usuario',
                    placeholder='Ingresa tu usuario'
                ).classes(
                    'w-full mb-4 '             
                    'text-[#1F2937] '           
                    'border border-gray-300 '   
                    'px-4 py-2 '                
                    'rounded focus:outline-none '        
                    'focus:ring-2 focus:ring-[#349CD7]'  
                )
                # password
                password_input = ui.input(
                    'Contraseña',
                    placeholder='Ingresa tu contraseña',
                    password=True
                ).classes(
                    'w-full mb-6 '
                    'text-[#1F2937] '
                    'border border-gray-300 '
                    'px-4 py-2 '
                    'rounded focus:outline-none '
                    'focus:ring-2 focus:ring-[#349CD7]'
                )

                # Button "Entrar"
                def submit_login():
                    usuario = username_input.value
                    clave = password_input.value
                    ui.notify(f'Has intentado iniciar sesión como "{usuario}".', position='top')

                ui.button('Entrar', on_click=submit_login).classes(
                    'w-full '                         # ancho completo dentro de la tarjeta
                    '!bg-[#349CD7] '
                    '!text-[#FAF9F6] '
                    'font-semibold '                  # texto en negrita
                    'px-4 py-2 '                      # padding interior
                    'rounded-lg '                     # bordes levemente redondeados
                    'focus:outline-none '             # quita el outline por defecto
                    'focus:ring-2 focus:ring-[#2C82C9]'  # anillo al hacer focus
                )

                # Secondary links
                with ui.row().classes('mt-4 justify-between w-[90%] sm:w-[95%]'):
                    ui.link('¿Olvidaste tu contraseña?', '/reset-password').classes(
                        'text-[#F59E0B] '           # naranja acento
                        'hover:text-[#D97706] '     # naranja acento más oscuro al pasar
                        'text-sm '
                    )
                    ui.link('Crear cuenta', '/register').classes(
                        'text-[#349CD7] '           # azul primario
                        'hover:text-[#2C82C9] '      # azul oscuro al pasar
                        'text-sm '
                    )
