from nicegui import ui
from frontend.services.auth_services import front_auth_service as auth    # Import the AuthService instance


# Function to create the registration Card
def register_card():
    # Submit function for registration
    def submit_register():
                        usuario = username_input.value
                        clave = password_input.value
                        ui.notify(f'Has intentado iniciar sesión como "{usuario}".', position='top')

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
                    '!bg-logo '                   
                    '!text-[#FAF9F6] '                 
                    'font-semibold '                  
                    'px-4 py-2 '                      
                    'rounded-lg '                     
                    'focus:outline-none '             
                    'focus:ring-2 focus:ring-[#2C82C9]'  
                )

                # Enlaces secundarios
                with ui.row().classes('mt-4 justify-between w-full'):
                    ui.link('Inicia Sesión', '/login').classes(
                        'text-[#F59E0B] '           # naranja acento
                        'hover:text-[#D97706] '     # naranja acento más oscuro al pasar
                        'text-sm'
                    )

# Function to create the login Card
def login_card():
    # Login card
            with ui.card().classes('bg-white p-8 rounded-lg shadow-lg max-w-md w-6/7 sm:w-full'):
                
                # Title
                ui.markdown('# Iniciar Sesión').classes(
                    'text-xs sm:text-2xl font-bold text-[#1F2937] mb-6 text-center'
                )

                # Input fields
                username_input = ui.input('User').classes(
                    'w-full mb-4 text-[#1F2937] border border-gray-300 px-4 py-2 '
                    'rounded focus:outline-none focus:ring-2 focus:ring-[#349CD7]'
                )

                password_input = ui.input('Password', password=True).classes(
                    'w-full mb-6 text-[#1F2937] border border-gray-300 px-4 py-2 '
                    'rounded focus:outline-none focus:ring-2 focus:ring-[#349CD7]'
                )

                # Feedback label
                feedback_label = ui.label().classes('text-sm mb-4')

                # Async function for login
                async def submit_login():
                    user = username_input.value
                    password = password_input.value

                    if not user or not password:
                        feedback_label.text = "Fill both fields"
                        feedback_label.style('color: red')
                        return
                    
                    # login_result = await auth.login(user, password)
                    await auth.login(user, password)
                    #feedback_label.text = str(login_result)  # For debugging
                    
                    # if login_result.get("success") == True:
                    #     feedback_label.text = f'Welcome, {user} 👋'
                    #     feedback_label.style('color: green')
                    #     # TODO: Save or redirect token here
                        
                    #     # Prueba de redirección a la página del calendario
                    #     ui.navigate.to('/calendar')
                    # else:
                    #     feedback_label.text = login_result
                    #     feedback_label.style('color: red')

                # Login button
                ui.button('Enter', on_click=submit_login).classes(
                                                                    'w-full '
                                                                    '!bg-[#349CD7] '
                                                                    '!text-[#FAF9F6] '
                                                                    'font-semibold px-4 py-2 '
                                                                    'rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2C82C9]'
                                                                )

                # Links
                with ui.row().classes('mt-4 justify-between w-[90%] sm:w-[95%]'):
                    
                    # Link to reset password
                    ui.link('Forgotten your password?', '/reset-password').classes(
                                                                                    'text-[#F59E0B] '
                                                                                    'hover:text-[#D97706] '
                                                                                    'text-sm'
                                                                                )
                    # Link to register
                    ui.link('Create account', '/register').classes(
                                                                    'text-[#349CD7] '
                                                                    'hover:text-[#2C82C9] '
                                                                    'text-sm'
                                                                )
