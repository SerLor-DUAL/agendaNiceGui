from nicegui import ui

def header_links():
    # Agrega aquí el CSS personalizado
    ui.add_head_html('<link rel="stylesheet" href="/static/css/styleColores.css">')
    # Add customs CSS for animation.
    ui.add_head_html('''
    <link rel="stylesheet" href="/static/css/animations.css">
    ''')