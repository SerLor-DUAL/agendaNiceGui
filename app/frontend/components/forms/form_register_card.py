# frontend/components/form_register_card.py

# Import necesary modules
from nicegui import ui                                                    # Import the ui module
from frontend.services.auth_services import front_auth_service as auth    # Import the AuthService instance
from frontend.utils.routing import front_router_handler as frh            # Importing the RouteHandler   

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to create the register form card component
def register_card():
    
    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # METHODS #
    
    async def submit_register():
        """Register method that sends a POST request to the backend to register a new user."""
        
        username_value = username_input.value
        password_value = password_input.value
        confirm_password_value = confirm_password_input.value

        if not username_value or not password_value or not confirm_password_value:
            feedback_label.text = "Rellene todos los campos"
            feedback_label.style('color: red')
            return
        
        if password_value != confirm_password_value:
            feedback_label.text = "Las contraseñas no coinciden"
            feedback_label.style('color: red')
            return
        
        result = await auth.register(username_value, password_value)

        # Updates the feedback label based on the result
        if result.get('status') == 'success':
            feedback_label.text = result.get('message', 'Inicio de sesión con éxito')
            feedback_label.style('color: green')
            username_input.value = ''
            password_input.value = ''
            
            frh.go_to('/diary')
            
        else:
            feedback_label.text = result.get('message', 'Error al registrarse')
            feedback_label.style('color: red')

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # UI #
    
    # Principal row
    with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
            
        # Register card
        with ui.card().classes('bg-white p-8 rounded-lg shadow-lg max-w-md w-5/6 sm:w-full '):
            
            # Register title
            ui.markdown('# Registrarse').classes(
                                                'text-xs '
                                                'sm:text-2xl '
                                                'font-bold '
                                                'text-[#1F2937] ' 
                                                'mb-6 text-center'
                                            )   
            
            # Username input
            username_input = ui.input('Usuario',).classes(
                                                                'w-full mb-4 '              
                                                                'text-[#1F2937] '           
                                                                'border border-gray-300 '   
                                                                'px-4 py-2 '                
                                                                'rounded focus:outline-none '        
                                                                'focus:ring-2 focus:ring-[#349CD7]'  
                                                            ).props('autofocus id="username" maxlength="100"')  # Autofocus on username input
            
            # Add JavaScript to change focus when pressing Enter
            ui.run_javascript("""
                document.querySelector('input[id="username"]').addEventListener('keydown', function(event) {
                    if (event.key === 'Enter') {
                        document.querySelector('input[id="password"]').focus();
                    }
                });
                document.querySelector('input[id="password"]').addEventListener('keydown', function(event) {
                    if (event.key === 'Enter') {
                        document.querySelector('input[id="confirm-password"]').focus();
                    }
                });
                document.querySelector('input[id="confirm-password"]').addEventListener('keydown', function(event) {
                    if (event.key === 'Enter') {
                        document.querySelector('button[id="register-button"]').focus();
                    }
                });
                              """)
            
            # Password input
            password_input = ui.input('Contraseña', password=True).classes(
                                                                            'w-full mb-4 '
                                                                            'text-[#1F2937] '
                                                                            'border border-gray-300 '
                                                                            'px-4 py-2 '
                                                                            'rounded focus:outline-none '
                                                                            'focus:ring-2 focus:ring-[#349CD7]'
                                                                        ).props('id="password" maxlength="100"')  # Password input with max length
            # Codigo mejorable para el botón de ojo de contraseña (refactorizar)
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
                    const pwInput = document.querySelector('input[id="password"]');
                    const eyeBtn = document.querySelector('#eye-button');
                              
                    let visible = false;
                    eyeBtn.addEventListener('click', function() {
                        visible = !visible;
                        pwInput.type = visible ? 'text' : 'password';
                    });
                }, 500);
            """)

            # Confirm password input
            confirm_password_input = ui.input('Confirmar Contraseña', password=True).classes(
                                                                                            'w-full mb-6 '
                                                                                            'text-[#1F2937] '
                                                                                            'border border-gray-300 '
                                                                                            'px-4 py-2 '
                                                                                            'rounded focus:outline-none '
                                                                                            'focus:ring-2 focus:ring-[#349CD7]'
                                                                                        ).props('id="confirm-password" maxlength="100"')  # Confirm password input with max length

            # Codigo mejorable para el botón de ojo de confirmación (refactorizar)
            with confirm_password_input:
                confirm_password_visible = ui.switch(value=False).props('dense').style('display:none')  # Estado oculto
                confirm_eye_button = ui.button(icon='visibility_off', on_click=lambda: confirm_toggle_password()).props('flat').classes('p-2 m-0 h-fit self-center rounded-lg').props('id="confirm-eye-button"')

            def confirm_toggle_password():
                confirm_password_visible.value = not confirm_password_visible.value
                if confirm_password_visible.value:
                    confirm_password_input.type = 'text'
                else:
                    confirm_password_input.type = 'password'
                confirm_eye_button.icon = 'visibility' if confirm_password_visible.value else 'visibility_off'

            # Add JavaScript to toggle password visibility
            ui.run_javascript("""
                // Espera a que el DOM esté listo
                setTimeout(function() {
                    const pwInput = document.querySelector('input[id="confirm-password"]');
                    const eyeBtn = document.querySelector('#confirm-eye-button');
                              
                    let visible = false;
                    eyeBtn.addEventListener('click', function() {
                        visible = !visible;
                        pwInput.type = visible ? 'text' : 'password';
                    });
                }, 500);
            """)

            # Register button
            ui.button('Registrarse', on_click=submit_register).classes(
                                                                        'w-full '                        
                                                                        '!bg-logo '                   
                                                                        '!text-[#FAF9F6] '                 
                                                                        'font-semibold '                  
                                                                        'px-4 py-2 '                      
                                                                        'rounded-lg '                     
                                                                        'focus:outline-none '             
                                                                        'focus:ring-2 focus:ring-[#2C82C9]'  
                                                                    ).props('id="register-button"')
            # Feedback label
            feedback_label = ui.label().classes('text-sm mb-4')

            # Secondary links row
            with ui.row().classes('mt-4 justify-between w-full'):
                
                # Login link
                ui.link('Iniciar Sesión', '/login').classes(
                                                        'text-[#F59E0B] '           
                                                        'hover:text-[#D97706] '    
                                                        'text-sm'
                                                    )

# ----------------------------------------------------------------------------------------------------------------------------------------- #
