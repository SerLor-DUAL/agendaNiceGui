# frontend/components/navbar.py

# Import necesary modules
from nicegui import ui              # Import the ui module

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to add the navbar component
def navbar():
    
    # Principal row
    with ui.row().classes('items-center justify-between bg-gray-800 p-4 text-white w-full rounded-t'):
        
        # Logo image
        img = ui.image('/static/img/logo.png').classes(
                                                        'w-16 h-auto rounded '
                                                        'cursor-pointer ' 
                                                        'hover:opacity-80 '
                                                        'transition-opacity duration-300' 
                                                        )
        
        # Logo click event
        img.on('click', lambda: ui.navigate.to('/'))
        
        
        # Second row
        with ui.row().classes('space-x-4'):
            
            # Login button
            ui.button( 'Login', on_click=lambda: ui.navigate.to('/login'),).classes( 
                                                                                        '!bg-[#349CD7] '
                                                                                        'text-[#FAF9F6] '
                                                                                        'px-4 '            
                                                                                        'py-2 '            
                                                                                        'rounded '         
                                                                                    )

            # Register button
            ui.button('Registro', on_click=lambda: ui.navigate.to('/register')).classes(
                                                                                            '!bg-[#349CD7] '
                                                                                            'text-[#FAF9F6] '            
                                                                                            'px-4 '                  
                                                                                            'py-2 '                  
                                                                                            'rounded'                
                                                                                        )

# ----------------------------------------------------------------------------------------------------------------------------------------- #