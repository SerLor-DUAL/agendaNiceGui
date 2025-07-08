# frontend/components/header_links.py

# Import necesary modules
from nicegui import ui      # Import the ui module

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to add header links to the HTML
def header_links():
    """Injects critical CSS and JS links directly into the HTML <head> dynamically using NiceGUI's `ui.add_head_html()`.

    WHY inline injection here instead of static files or global headers?

    1. **Tailwind CDN and config must load in proper order:**
        - Tailwind's JS injects styles dynamically.
        - Inline config script must run immediately after Tailwind to apply custom theme colors.
        - Loading Tailwind or config externally can lead to the config being ignored or overridden.

    2. **Custom CSS must load after Tailwind to override default styles:**
        - Injecting CSS inline here guarantees styles load at the right time and with proper specificity.
        - Styles to hide scrollbars or custom colors need to override Tailwind's defaults.

    3. **Static CSS files are linked for additional styles and animations:**
        - These are loaded separately but after Tailwind and core inline CSS.
        - If conflicts occur, inline styles have priority.

    This approach ensures consistent style application and avoids issues with CSS/JS order or caching
    problems that might happen if files are loaded only in external headers or static files.

    Usage:
        Call `header_links()` once during app initialization to set up the frontend styles and scripts.
    """
    
    # Load Tailwind CSS from CDN with custom theme config inline
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

    # Inject critical CSS inline for hiding scrollbars with high specificity and priority
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
                                    width: 0 !important;
                                    height: 0 !important;
                                    pointer-events: none !important;
                                    transition: none !important;
                                }

                        </style>
                    """)

    # Link external static CSS files for colors and animations
    # Note: If tailwind.config works properly, styleColores.css may be commented out temporarily
    ui.add_head_html('<link rel="stylesheet" href="/static/css/styleColores.css">')
    ui.add_head_html('<link rel="stylesheet" href="/static/css/animations.css">')
    
# ----------------------------------------------------------------------------------------------------------------------------------------- #