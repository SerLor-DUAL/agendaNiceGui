# frontend/components/navbar_buttons.py

# Import necesary modules
from nicegui import ui                                                      # Import the ui module
from frontend.services.auth_services import front_auth_service as auth      # Importing the AuthService instance

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to add the navbar buttons component
async def navbar_buttons():
    
    # Check if the user is logged
    logged = await auth.auth_required(check_only=True)
    
    # If the user is not logged in, add the logout button
    if logged:
        # Logout button
        ui.button( 'Logout', on_click=lambda: ui.navigate.to('/logout'),).classes( 
                                                                                    '!bg-[#349CD7] '
                                                                                    'text-[#FAF9F6] '
                                                                                    'px-4 '            
                                                                                    'py-2 '            
                                                                                    'rounded '         
                                                                                )

    # If the user is logged in, add the login and register buttons
    else:
        
        # Login button
        ui.button( 'Login', on_click=lambda: ui.navigate.to('/login'),).classes( 
                                                                                    '!bg-[#349CD7] '
                                                                                    'text-[#FAF9F6] '
                                                                                    'px-4 '            
                                                                                    'py-2 '            
                                                                                    'rounded '         
                                                                                )

        # Register button
        ui.button('Register', on_click=lambda: ui.navigate.to('/register')).classes(
                                                                                        '!bg-[#349CD7] '
                                                                                        'text-[#FAF9F6] '            
                                                                                        'px-4 '                  
                                                                                        'py-2 '                  
                                                                                        'rounded'                
                                                                                    )
