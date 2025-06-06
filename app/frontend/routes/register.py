from nicegui import ui
from ..components.navbar import navbar

def create_register_page():
    # Agrega aquí el CSS personalizado
    ui.add_head_html('<link rel="stylesheet" href="/static/css/styleColores.css">')
    # Submit function for registration
    def submit_register():
                        usuario = username_input.value
                        clave = password_input.value
                        ui.notify(f'Has intentado iniciar sesión como "{usuario}".', position='top')
    with ui.column().classes('w-full h-screen bg-gray-100'):
        navbar()

        
        with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
            with ui.card().classes('bg-white p-8 rounded-lg shadow-lg max-w-md w-5/6 sm:w-full '):
                ui.markdown('# Registrarse').classes(
                'text-xs sm:text-2xl font-bold text-[#1F2937] mb-6 text-center'
                )   
                # Username
                username_input = ui.input(
                    'Usuario',
                ).classes(
                    'w-full mb-4 '              
                    'text-[#1F2937] '           
                    'border border-gray-300 '   
                    'px-4 py-2 '                
                    'rounded focus:outline-none '        
                    'focus:ring-2 focus:ring-[#349CD7]'  

                )
                # Password
                password_input = ui.input(
                    'Contraseña',
                    password=True
                ).classes(
                    'w-full mb-4 '
                    'text-[#1F2937] '
                    'border border-gray-300 '
                    'px-4 py-2 '
                    'rounded focus:outline-none '
                    'focus:ring-2 focus:ring-[#349CD7]'
                )
                # Confirm Password
                password_input = ui.input(
                    'Confirmar Contraseña',
                    password=True
                ).classes(
                    'w-full mb-6 '
                    'text-[#1F2937] '
                    'border border-gray-300 '
                    'px-4 py-2 '
                    'rounded focus:outline-none '
                    'focus:ring-2 focus:ring-[#349CD7]'
                )

    
                ui.button('Registrarse', on_click=submit_register).classes(
                    'w-full '                        
                    '!bg-[#349CD7] '                   
                    '!text-[#FAF9F6] '                 
                    'font-semibold '                  
                    'px-4 py-2 '                      
                    'rounded-lg '                     
                    'focus:outline-none '             
                    'focus:ring-2 focus:ring-[#2C82C9]'  
                )

                # Enlaces secundarios
                with ui.row().classes('mt-4 justify-between w-full'):
                    ui.link('Inicia Sesión', '/reset-password').classes(
                        'text-[#F59E0B] '           # naranja acento
                        'hover:text-[#D97706] '     # naranja acento más oscuro al pasar
                        'text-sm'
                    )
                
                