# frontend/components/header_links.py

# Import necesary modules
from nicegui import ui      # Import the ui module

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to add header links to the HTML
def header_links():
    
    # Add Tailwind CSS
    ui.add_head_html('''
                        <script src="https://cdn.tailwindcss.com"></script>
                        <script>
                            tailwind.config = {
                                theme: {
                                    extend: {
                                        colors: {
                                            'logo': '#349CD7',
                                            'secondary': '#2C82C9',
                                            'lightBlue': '#8ED6F8',
                                            'darkGray': '#1F2937',
                                            'midGray': '#4B5563',
                                            'lightGray': '#F3F4F6',
                                            'AccentOrange': '#FFFFFF',
                                            'AccentGreen': '#10B981'
                                            }
                                    }
                                }
                            }
                        </script>
                    ''')

    ui.add_head_html("""
                        <style>
                                .hide-scroll .q-scrollarea__container {
                                    scrollbar-width: none !important;       /* Firefox */
                                    -ms-overflow-style: none !important;    /* IE 10+ */
                                    overflow-y: scroll !important;
                                }

                                .hide-scroll .q-scrollarea__container::-webkit-scrollbar {
                                    width: 0px !important;
                                    height: 0px !important;
                                    display: none !important;
                                }

                                .hide-scroll .q-scrollarea__thumb {
                                    display: none !important;
                                    opacity: 0 !important;
                                    width: 0px !important;
                                    height: 0px !important;
                                }
                        </style>
                        """)

    # Add customs CSS
    # Comentar este link si el tailwind.config de arriba funciona (Por el momento no funciona ninguno de los dos ??)
    ui.add_head_html('<link rel="stylesheet" href="/static/css/styleColores.css">')
    
    # Add customs CSS for animation.
    ui.add_head_html('''
                        <link rel="stylesheet" href="/static/css/animations.css">
                    ''')
    
# ----------------------------------------------------------------------------------------------------------------------------------------- #