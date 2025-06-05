from nicegui import ui
from ..components.navbar import navbar

def create_home_page():
    navbar()

    with ui.row().classes(
    'flex '                
    'items-center '        
    'justify-between '    
    'min-h-screen '        
    'px-8 '           
    'bg-gray-50 '         
    'w-full'                
    ):
        with ui.column().classes(
            'flex-1 ',          
            'pr-8 ',             
            'text-center ',      
            'md:text-left'       
        ):
            ui.markdown('# AgendaNiceGUI').classes(
                'text-5xl ',
                'font-extrabold ',
                'text-gray-900 ',
                'mb-4'
            )
            ui.markdown('Esta agenda es nuestra brújula. 🧭').classes(
                'text-lg ',
                'text-gray-700'
            )

        with ui.column().classes(
            'flex-1 ',           
            'pl-8 ',             
            'text-center ',      
            'md:text-right'      
        ):
            ui.image('/static/img/hero.png').classes(
                'max-w-full ',    
                'h-auto ',        
                'mx-auto ',       
                'md:mx-0'         
            )

    