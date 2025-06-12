# frontend/components/header_links.py

# Import necesary modules
from nicegui import ui      # Import the ui module

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: Function to add header links to the HTML
def header_links():
    
    # Add customs CSS
    ui.add_head_html('<link rel="stylesheet" href="/static/css/styleColores.css">')
    
    # Add customs CSS for animation.
    ui.add_head_html('''
                        <link rel="stylesheet" href="/static/css/animations.css">
                    ''')
    
# ----------------------------------------------------------------------------------------------------------------------------------------- #