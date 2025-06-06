from nicegui import ui
from ..components.navbar import navbar

def create_home_page():
    navbar()
    # Add customs CSS for animation.
    ui.add_head_html('''
    <link rel="stylesheet" href="/static/css/animations.css">
    ''')
    with ui.row().classes(
    'flex '                
    'items-center '        
    'justify-between '    
    'h-[80%] '        
    'px-8 '           
    'bg-gray-50 '         
    'w-full'                
    ):
        with ui.column().classes(
            'flex-1 '          
            'pr-8 '             
            'text-center '
            'h-full '             
        ):
            ui.label('AgendaNiceGUI').classes(
                'text-4xl md:text-6xl lg:text-8xl '
                'font-bold '
                'text-gray-900 '
                'mb-12 w-full '
                 'slide-in-left'
            ).style(
                # Podemos escalonar la entrada de este texto (delay = 0s)
                'animation-delay: 0s;'
            )
            ui.label('Esta agenda es nuestra brújula. 🧭').classes(
                '!text-3xl '
                'text-gray-700 w-full '
                'slide-in-left'
            ).style(
                # Podemos escalonar la entrada de este texto (delay = 0s)
                'animation-delay: 0s;'
            )

        with ui.column().classes(
            'flex-1 '           
            'pl-8 '             
            'text-center '      
            'md:text-right'      
        ):
            ui.image('/static/img/hero.png').classes(      
                'w-[90%] h-[90%] p-4 mx-auto m-4 rounded-xl'
            )

    