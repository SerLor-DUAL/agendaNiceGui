# frontend/components/form_login_card.py

# Import necesary modules
from nicegui import ui                                                    # Import the ui module
from frontend.services.auth_services import front_auth_service as auth    # Import the AuthService instance

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
            feedback_label.text = "Fill both fields"
            feedback_label.style('color: red')
            return
        
        # Updates the feedback label
        feedback_label.text = "Logging in..."
        feedback_label.style('color: black')

        result = await auth.login(user, password)
        
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
    
        # Login card
        with ui.card().classes('bg-white p-8 rounded-lg shadow-lg max-w-md w-6/7 sm:w-full'):
            
            # Login Title
            ui.markdown('# Login').classes(
                                                'text-xs '
                                                'sm:text-2xl '
                                                'font-bold '
                                                'text-[#1F2937] '
                                                'mb-6 '
                                                'text-center'
                                            )

            # Input fields
            username_input = ui.input('User').classes(
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
                                                    )

            # Password input
            password_input = ui.input('Password', password=True).classes(
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

            # Feedback label
            feedback_label = ui.label().classes('text-sm mb-4')

            # Login button
            ui.button('Enter', on_click=submit_login).classes(
                                                                'w-full '
                                                                '!bg-[#349CD7] '
                                                                '!text-[#FAF9F6] '
                                                                'font-semibold px-4 py-2 '
                                                                'rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2C82C9]'
                                                            )

            # Secondary links row
            with ui.row().classes('mt-4 justify-between w-[90%] sm:w-[95%]'):
                
                # Reset password link
                ui.link('Forgotten your password?', '/reset-password').classes(
                                                                                    'text-[#F59E0B] '
                                                                                    'hover:text-[#D97706] '
                                                                                    'text-sm'
                                                                                )
                # Register link
                ui.link('Create account', '/register').classes(
                                                                'text-[#349CD7] '
                                                                'hover:text-[#2C82C9] '
                                                                'text-sm'
                                                            )

# ----------------------------------------------------------------------------------------------------------------------------------------- #