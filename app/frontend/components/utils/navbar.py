# frontend/components/navbar.py

# Import necesary modules
from nicegui import ui, app                                                                     # Import the ui module
from frontend.components.utils.navbar_buttons import navbar_buttons, mobile_nav_buttons     # Importing the navbar_buttons component
from frontend.components.utils.navbar_links import navbar_links, mobile_nav_links           # Importing the navbar_links component
from frontend.utils.routing import front_router_handler as frh                              # Importing the RouteHandler

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to add the navbar component
async def navbar():
    current_user =  app.storage.user.get('user_id', None)
    # Header
    with ui.header().classes('bg-gray-900 text-white shadow-md'):
        
            # Container
            with ui.row().classes('items-center justify-between px-6 py-4 w-full'):
                
                # Logo (LEFT)
                with ui.row().classes('flex items-center flex-1'):
                    img = ui.image('/static/img/logo.png').classes('w-14 h-auto rounded-lg cursor-pointer hover:opacity-80 transition-opacity duration-300')
                    img.on('click', lambda: frh.go_to('/'))

                # Links (CENTER)
                with ui.row().classes('items-center justify-center space-x-8 flex-1 max-lg:hidden'):
                    with ui.row().classes('space-x-6 text-lg font-medium'):
                        await navbar_links(current_user)

                # Botones (RIGHT)
                with ui.row().classes('items-center justify-end space-x-4 flex-1 max-lg:hidden'):
                    await navbar_buttons(current_user)
                
                # ----------------------------------------------------------------------------------------------------------------------------------------- #
                # Mobile
                
                with ui.element('div').classes('lg:hidden relative'):
                    
                    # Menu button
                    menu_button = ui.button().classes('text-white bg-transparent hover:bg-gray-700 p-2 rounded-md transition-colors duration-200')
                    
                    # Hamburguer Logo
                    with menu_button:
                        ui.label('☰').classes('text-white text-3xl leading-none select-none')

                    # Overlay of menu
                    mobile_overlay = ui.element('div').classes('fixed inset-0 bg-black/50 backdrop-blur-md z-50 hidden')

                    # Sliding mobile menu
                    mobile_menu = ui.element('div').classes(
                                                                'fixed top-0 right-0 h-full w-80 max-w-[85vw] bg-gray-900 text-white shadow-2xl z-50 '
                                                                'transform transition-transform duration-300 ease-in-out translate-x-full'
                                                            )

                    with mobile_menu:
                        
                        # Header Mobile
                        with ui.row().classes('flex justify-between items-center p-4 border-b border-gray-700'):
                            
                            #Title
                            ui.label('Menú').classes('text-xl font-semibold')
                            
                            # Close button menu
                            close_btn = ui.button('✕').classes('text-white bg-transparent hover:bg-gray-700 p-2 rounded-full text-xl')

                        # Mobile elements
                        with ui.column().classes('p-4 space-y-4 flex-1 items-center'):
                            
                            # Links
                            with ui.column().classes('space-y-1'):
                                await mobile_nav_links(current_user)
                                
                            ui.separator().classes('my-2 border-gray-700')
                            
                            # Buttons
                            with ui.column().classes('space-y-2'):
                                await mobile_nav_buttons(current_user)

                    # State to open/close menu
                    is_menu_open = False

                    def toggle_mobile_menu():
                        """ Function to manage the opening/closing of the mobile menu"""
                        nonlocal is_menu_open
                        is_menu_open = not is_menu_open
                        if is_menu_open:
                            mobile_overlay.classes(remove='hidden')
                            mobile_menu.classes(remove='translate-x-full')
                            mobile_menu.classes(add='translate-x-0')
                            ui.run_javascript("document.body.classList.add('overflow-hidden')")
                        else:
                            mobile_overlay.classes(add='hidden')
                            mobile_menu.classes(remove='translate-x-0')
                            mobile_menu.classes(add='translate-x-full')
                            ui.run_javascript("document.body.classList.remove('overflow-hidden')")

                    # Events for the menu
                    menu_button.on('click', toggle_mobile_menu)         # Hamburguer button
                    close_btn.on('click', toggle_mobile_menu)           # Close button inside menu
                    mobile_overlay.on('click', toggle_mobile_menu)      # Outside click
                    
                # ----------------------------------------------------------------------------------------------------------------------------------------- #