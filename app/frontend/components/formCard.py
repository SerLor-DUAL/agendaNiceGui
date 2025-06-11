from nicegui import ui
import httpx

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

                    # Url and json data to send to the API
                    url = "http://127.0.0.1:8081/api/loginJSON"
                    json_data = {"nickname": user, "password": password}

                    async with httpx.AsyncClient() as client:
                        try:
                            response = await client.post(url, json=json_data, timeout=10)
                            
                            # Check if the request was successful
                            if response.status_code == 200:
                                
                                # Access token and refresh token
                                data = response.json()
                                access_token = data.get("access_token")
                                refresh_token = data.get("refresh_token")

                                if access_token and refresh_token:
                                    feedback_label.text = f'Welcome, {user} 👋'
                                    feedback_label.style('color: green')
                                    # TODO: Save or redirect token here
                                    # Prueba de redirección a la página del calendario
                                    ui.navigate.to('/calendar')
                                else:
                                    feedback_label.text = "Error: Token not found"
                                    feedback_label.style('color: red')

                            else:
                                feedback_label.text = "Error: Incorrect credencials"
                                feedback_label.style('color: red')

                        except Exception as e:
                            feedback_label.text = f"Connection error: {e}"
                            feedback_label.style('color: red')

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
