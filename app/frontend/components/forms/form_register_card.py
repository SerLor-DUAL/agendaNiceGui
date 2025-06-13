# frontend/components/form_register_card.py

# Import necesary modules
from nicegui import ui                                                    # Import the ui module
from frontend.services.auth_services import front_auth_service as auth    # Import the AuthService instance

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
            feedback_label.text = "Fill all fields"
            feedback_label.style('color: red')
            return
        
        if password_value != confirm_password_value:
            feedback_label.text = "Passwords do not match"
            feedback_label.style('color: red')
            return
        
        result = await auth.register(username_value, password_value)

        # Updates the feedback label based on the result
        if result.get('status') == 'success':
            feedback_label.text = result.get('message', 'Login successful')
            feedback_label.style('color: green')
            username_input.value = ''
            password_input.value = ''
            
            # Redirects the user to the calendar page
            ui.navigate.to('/calendar')
            
        else:
            feedback_label.text = result.get('message', 'Error logging in')
            feedback_label.style('color: red')

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # UI #
    
    # Principal row
    with ui.row().classes('items-center justify-center w-full h-[80vh] bg-gray-100'):
            
        # Register card
        with ui.card().classes('bg-white p-8 rounded-lg shadow-lg max-w-md w-5/6 sm:w-full '):
            
            # Register title
            ui.markdown('# Register').classes(
                                                'text-xs '
                                                'sm:text-2xl '
                                                'font-bold '
                                                'text-[#1F2937] ' 
                                                'mb-6 text-center'
                                            )   
            
            # Username input
            username_input = ui.input('Username',).classes(
                                                                'w-full mb-4 '              
                                                                'text-[#1F2937] '           
                                                                'border border-gray-300 '   
                                                                'px-4 py-2 '                
                                                                'rounded focus:outline-none '        
                                                                'focus:ring-2 focus:ring-[#349CD7]'  
                                                            )
            
            # Password input
            password_input = ui.input('Password', password=True).classes(
                                                                            'w-full mb-4 '
                                                                            'text-[#1F2937] '
                                                                            'border border-gray-300 '
                                                                            'px-4 py-2 '
                                                                            'rounded focus:outline-none '
                                                                            'focus:ring-2 focus:ring-[#349CD7]'
                                                                        )
            # Confirm password input
            confirm_password_input = ui.input('Confirm Password', password=True).classes(
                                                                                            'w-full mb-6 '
                                                                                            'text-[#1F2937] '
                                                                                            'border border-gray-300 '
                                                                                            'px-4 py-2 '
                                                                                            'rounded focus:outline-none '
                                                                                            'focus:ring-2 focus:ring-[#349CD7]'
                                                                                        )

            

            # Register button
            ui.button('Register', on_click=submit_register).classes(
                                                                        'w-full '                        
                                                                        '!bg-logo '                   
                                                                        '!text-[#FAF9F6] '                 
                                                                        'font-semibold '                  
                                                                        'px-4 py-2 '                      
                                                                        'rounded-lg '                     
                                                                        'focus:outline-none '             
                                                                        'focus:ring-2 focus:ring-[#2C82C9]'  
                                                                    )
            # Feedback label
            feedback_label = ui.label().classes('text-sm mb-4')

            # Secondary links row
            with ui.row().classes('mt-4 justify-between w-full'):
                
                # # Register link
                # ui.link('Register', '/register').classes(
                #                                             'text-[#F59E0B] '           
                #                                             'hover:text-[#D97706] '    
                #                                             'text-sm'
                #                                         )

                # Login link
                ui.link('Iniciar Sesión', '/login').classes(
                                                        'text-[#F59E0B] '           
                                                        'hover:text-[#D97706] '    
                                                        'text-sm'
                                                    )

# ----------------------------------------------------------------------------------------------------------------------------------------- #
