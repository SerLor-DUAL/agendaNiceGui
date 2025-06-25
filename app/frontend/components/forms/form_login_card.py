# frontend/components/form_login_card.py

# Import necesary modules
from nicegui import ui                                                    # Import the ui module
from frontend.services.auth_services import front_auth_service as auth    # Import the AuthService instance
from frontend.utils.routing import front_router_handler as frh            # Importing the RouteHandler   

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to create the login form card component
def login_card():
    
    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # METHODS #
    async def submit_login():
        """ Login method that sends a POST request to the backend to login the user. It obtains cookies for the browser using a JavaScript fetch. """
        
        user = username_input.value
        password = password_input.value

        if not user or not password:
            feedback_label.text = "Rellene todos los campos"
            feedback_label.style('color: red')
            return
        
        # Updates the feedback label
        feedback_label.text = "Iniciando sesión..."
        feedback_label.style('color: black')

        result = await auth.login(user, password)
        
        # Updates the feedback label based on the result
        if result.get('status') == 'success':
            feedback_label.text = result.get('message', 'Inicio de sesión exitoso')
            feedback_label.style('color: green')
            username_input.value = ''
            password_input.value = ''
            
            # Redirects the user to the calendar page
            frh.go_to('/diary')
            
            
        else:
            feedback_label.text = result.get('message', 'Error al iniciar sesión')
            feedback_label.style('color: red')
    
    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # UI #
    
    # Principal row
    with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
    
        # Login card
        with ui.card().classes('bg-white p-8 rounded-lg shadow-lg max-w-md w-6/7 sm:w-full'):
            
            # Login Title
            ui.markdown('# Iniciar Sesión').classes(
                                                'text-xs '
                                                'sm:text-2xl '
                                                'font-bold '
                                                'text-[#1F2937] '
                                                'mb-6 '
                                                'text-center'
                                            )

            # Input fields
            username_input = ui.input('Usuario').classes(
                                                        'w-full '
                                                        'mb-4 '
                                                        'text-[#1F2937] '
                                                        'border '
                                                        'border-gray-300 '
                                                        'px-4 '
                                                        'py-2 '
                                                        'rounded '
                                                        'focus:outline-none '
                                                        'focus:ring-2 '
                                                        'focus:ring-[#349CD7]'
                                                    ).props('autofocus id="username" maxlength="100"')  # Autofocus on username input
            
            # Al presionar Enter en username, enfoca password (Rehacer correctamente)
            ui.run_javascript("""
                document.querySelector('input[id="username"]').addEventListener('keydown', function(event) {
                    if (event.key === 'Enter') {
                        document.querySelector('input[type="password"]').focus();
                    }
                });
                              """)

            # Password input
            password_input = ui.input('Contraseña', password=True).classes(
                                                                            'w-full '
                                                                            'mb-6 '
                                                                            'text-[#1F2937] '
                                                                            'border '
                                                                            'border-gray-300 '
                                                                            'px-4 '
                                                                            'py-2 '
                                                                            'rounded '
                                                                            'focus:outline-none '
                                                                            'focus:ring-2 '
                                                                            'focus:ring-[#349CD7]'
                                                                        )
            # Al presionar Enter en password, enfoca el botón
            ui.run_javascript("""
                document.querySelector('input[type="password"]').addEventListener('keydown', function(event) {
                    if (event.key === 'Enter') {
                        document.querySelector('button[id="login-button"]').click();
                    }
                });
                """)
            with password_input:
                password_visible = ui.switch(value=False).props('dense').style('display:none')  # Estado oculto
                eye_button = ui.button(icon='visibility_off', on_click=lambda: toggle_password()).props('flat').classes('p-2 m-0 h-fit self-center rounded-lg').props('id="eye-button"')

            def toggle_password():
                password_visible.value = not password_visible.value
                if password_visible.value:
                    password_input.type = 'text'
                else:
                    password_input.type = 'password'
                eye_button.icon = 'visibility' if password_visible.value else 'visibility_off'

            # Add JavaScript to toggle password visibility
            ui.run_javascript("""
                // Espera a que el DOM esté listo
                setTimeout(function() {
                    const pwInput = document.querySelector('input[type="password"], input[type="text"][placeholder="Password"]');
                    const eyeBtn = document.querySelector('#eye-button');
                              
                    let visible = false;
                    eyeBtn.addEventListener('click', function() {
                        visible = !visible;
                        pwInput.type = visible ? 'text' : 'password';
                    });
                }, 500);
            """)
            
            # Feedback label
            feedback_label = ui.label().classes('text-sm mb-4')

            # Login button
            login_button = ui.button('Iniciar sesión', on_click=submit_login).classes(
                                                                'w-full '
                                                                '!bg-[#349CD7] '
                                                                '!text-[#FAF9F6] '
                                                                'font-semibold px-4 py-2 '
                                                                'rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2C82C9]'
                                                                'submit-button'
                                                            ).props('id="login-button" type="submit')

            # Secondary links row
            with ui.row().classes('mt-4 justify-between w-[90%] sm:w-[95%]'):
                
                # Reset password link
                ui.link('¿Se ha olvidado de su contraseña?', '/reset-password').classes(
                                                                                    'text-[#F59E0B] '
                                                                                    'hover:text-[#D97706] '
                                                                                    'text-sm'
                                                                                )
                # Register link
                ui.link('Crear una cuenta nueva', '/register').classes(
                                                                'text-[#349CD7] '
                                                                'hover:text-[#2C82C9] '
                                                                'text-sm'
                                                            )

# ----------------------------------------------------------------------------------------------------------------------------------------- #