# frontend/components/diary/events/events_list.py

# Import necessary modules
from nicegui import ui                      # Import NiceGUI
from .event_card import event_card          # Import the event_card function

def events_list(events, date_title=None, on_add=None, on_edit=None, on_delete=None, is_monthly=False):
    
    # Create a row for the events list container
    if date_title:
        with ui.row().classes('w-full items-center justify-between mb-4'):
            ui.label(f'Eventos de {date_title}').classes('text-lg font-bold text-gray-800')
            if on_add:
                ui.button(icon='add', color='green', on_click=on_add) \
                    .props('dense round') \
                    .classes('bg-green-500 hover:bg-green-600') \
                    .tooltip('Agregar evento')
    
    # Create the events list for the selected day
    if events:
        for event in events:
            event_card(event, 
                    on_edit=lambda e, ev=event: on_edit(ev) if on_edit else None,
                    on_delete=lambda e, ev=event: on_delete(ev) if on_delete else None,
                    is_monthly=is_monthly)
    
    # Show a message if there are no events
    else:
        
        # Create a column for the no events message
        with ui.column().classes('w-full items-center py-8 text-center'):
            ui.icon('event_busy', size='48px').classes('text-gray-300 mb-2')
            ui.label('No hay eventos programados' if not is_monthly else 'No hay eventos este mes').classes('text-gray-500 font-medium')
            if on_add and not is_monthly:
                ui.label('Haz clic en "+" para agregar uno').classes('text-gray-400 text-sm')