# frontend/components/diary/events/event_dialog.py

# Import necessary modules
from nicegui import ui      # Import the ui module from nicegui

def show_event_dialog(action, event_data, on_save, on_delete=None):
    
    title = {
                'create': 'Agregar evento',
                'edit': 'Editar evento',
                'delete': 'Eliminar evento'
                
            }[action]
            
    button_text = {
                        'create': 'Crear evento',
                        'edit': 'Guardar cambios',
                        'delete': 'Eliminar'
                        
                    }[action]
    
    button_color = {
                        'create': 'green',
                        'edit': 'blue',
                        'delete': 'red'
                        
                    }[action]

    # Create the dialog (Modal)
    with ui.dialog() as dialog, ui.card().classes('w-[500px] p-6'):
        
        # Dialog title
        ui.label(f'{title} - Día {event_data["day"]}').classes('text-xl font-bold mb-6 text-gray-800')

        # Dialog content for delete
        if action == 'delete':
            
            # Confirmation message
            ui.label('¿Estás seguro de que quieres eliminar este evento?').classes('text-gray-700 mb-3')
            
            # Event details
            with ui.card().classes('bg-red-50 border-l-4 border-red-400 p-4 mb-4'):
                ui.label(event_data.get('titulo', '')).classes('font-semibold text-red-800')
                ui.label(event_data.get('descripcion', '')).classes('text-sm text-red-700')
                ui.label(format_time_range(event_data.get('start_date', ''), event_data.get('end_date', ''))).classes('text-xs text-red-600')
                
        # Dialog content for create and edit
        else:
            
            # Title and description
            title_input = ui.input('Título del evento', value=event_data.get('titulo', '')).classes('w-full mb-4').props('outlined')
            description_input = ui.textarea('Descripción', value=event_data.get('descripcion', '')).classes('w-full mb-4').props('outlined')
            
            # Time range
            with ui.row().classes('w-full gap-4 mb-4'):
                
                # Start date
                with ui.column().classes('flex-1'):
                    ui.label('Fecha y hora de inicio').classes('text-sm font-medium text-gray-700 mb-2')
                    
                    # Inputs
                    start_date_input = ui.input('Fecha inicio', value=event_data.get('start_date', '').split(' ')[0] if event_data.get('start_date') else '') \
                        .classes('w-full mb-2').props('outlined').tooltip('Formato: dd/mm/aaaa')
                    start_time_input = ui.input('Hora inicio', value=event_data.get('start_date', '').split(' ')[1] if event_data.get('start_date') else '') \
                        .classes('w-full').props('outlined').tooltip('Formato: hh:mm')
                
                # End date
                with ui.column().classes('flex-1'):
                    ui.label('Fecha y hora de fin').classes('text-sm font-medium text-gray-700 mb-2')
                    
                    # Inputs
                    end_date_input = ui.input('Fecha fin', value=event_data.get('end_date', '').split(' ')[0] if event_data.get('end_date') else '') \
                        .classes('w-full mb-2').props('outlined').tooltip('Formato: dd/mm/aaaa')
                    end_time_input = ui.input('Hora fin', value=event_data.get('end_date', '').split(' ')[1] if event_data.get('end_date') else '') \
                        .classes('w-full').props('outlined').tooltip('Formato: hh:mm')
        
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------- #
        
        # Dialog actions
        with ui.row().classes('w-full justify-end gap-3 mt-6'):
            
            # Cancel button
            ui.button('Cancelar', on_click=dialog.close).props('flat').classes('text-gray-600 px-4')
            
            # Confirm delete button
            if action == 'delete':
                ui.button(button_text, on_click=lambda: on_delete(event_data)).classes(f'bg-red-500 text-white hover:bg-red-600 px-6')
            
            # Handle action for create and edit
            else:
                def handle_action():
                    new_event = {
                                    'titulo': title_input.value,
                                    'descripcion': description_input.value,
                                    'start_date': f'{start_date_input.value} {start_time_input.value}',
                                    'end_date': f'{end_date_input.value} {end_time_input.value}'
                                }
                    on_save(new_event)
                    dialog.close()
                
                # Save button
                ui.button(button_text, on_click=handle_action).classes(f'bg-{button_color}-500 text-white hover:bg-{button_color}-600 px-6')
    
    return dialog

def format_time_range(start_date, end_date):
    """ Formats time range for display """
    
    # Formats the time range to show it in a readable way
    try:
        start_time = start_date.split(' ')[1]
        end_time = end_date.split(' ')[1]
        return f"{start_time} - {end_time}"
    except:
        return "Todo el día"