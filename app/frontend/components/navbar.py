from nicegui import ui



def navbar():
    with ui.row().classes(
        'items-center '     
        'justify-between '    
        'bg-gray-800 '        
        'p-4 '               
        'text-white '         
        'w-full '
        'rounded-t'              
    ):
        img = ui.image('/static/img/logo.png').classes(
            'w-16 h-auto rounded '
            'cursor-pointer ' 
            'hover:opacity-80 '
            'transition-opacity duration-300' 
            )
        img.on('click', lambda: ui.navigate.to('/'))
        with ui.row().classes(
            'space-x-4' 
        ):
            # Botón de Iniciar Sesión
            ui.button(
                'Iniciar Sesión', 
                on_click=lambda: ui.navigate.to('/login'),
            ).classes( 
                 '!bg-[#349CD7] '
                 'text-[#FAF9F6] '
                 'px-4 '            
                 'py-2 '            
                 'rounded '         
            )

            # Botón de Registro
            ui.button('Registro', on_click=lambda: ui.navigate.to('/register')).classes(
                 '!bg-[#349CD7] '
                 'text-[#FAF9F6] '            
                 'px-4 '                  
                 'py-2 '                  
                 'rounded'                
            )
 