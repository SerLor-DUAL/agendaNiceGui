# frontend/components/diary/events/event_card.py

# Import necessary modules
from nicegui import ui        # Import the ui module

def event_card(event, on_edit=None, on_delete=None, is_monthly=False):
    """ Creates a card for an event with optional edit and delete buttons, and it's information """
    
    # Card styles
    card_classes = 'w-full mb-2 p-3 bg-indigo-50 border-l-4 border-indigo-500 hover:bg-indigo-100 transition-colors'
    if not is_monthly:
        card_classes = 'w-full mb-3 p-4 bg-blue-50 border-l-4 border-blue-500 hover:bg-blue-100 transition-colors'
    
    # Event card
    with ui.card().classes(card_classes):
        
        # Card content
        with ui.row().classes('w-full items-start justify-between'):
            
            # Event info
            with ui.column().classes('flex-1 gap-1'):
                
                # Title
                ui.label(event['titulo']).classes('text-sm font-semibold text-gray-800' if is_monthly else 'text-base font-semibold text-gray-800')
                
                # Description
                if event.get('descripcion'):
                    ui.label(event['descripcion']).classes('text-xs text-gray-600' if is_monthly else 'text-sm text-gray-600')
                    
                # Time range
                ui.label(format_time_range(event['start_date'], event['end_date'])) \
                    .classes('text-xs text-indigo-600 font-medium' if is_monthly else 'text-xs text-blue-600 font-medium')
            
            # Actions
            if on_edit or on_delete:
                
                # Edit and delete row 
                with ui.row().classes('gap-1 ml-2'):
                    
                    # Edit
                    if on_edit:
                        btn_size = 'size=xs' if is_monthly else ''
                        ui.button(icon='edit', on_click=lambda: on_edit(event)) \
                            .props(f'dense round flat {btn_size}') \
                            .classes('text-indigo-600 hover:bg-indigo-200' if is_monthly else 'text-blue-600 hover:bg-blue-200') \
                            .tooltip('Editar evento')
                            
                    # Delete
                    if on_delete:
                        btn_size = 'size=xs' if is_monthly else ''
                        ui.button(icon='delete', on_click=lambda: on_delete(event)) \
                            .props(f'dense round flat {btn_size}') \
                            .classes('text-red-600 hover:bg-red-200') \
                            .tooltip('Eliminar evento')


def format_time_range(start_date, end_date):
    """Formats time range for display in the card"""
    
    # Formats the time range to show it in a readable way
    try:
        start_time = start_date.split(' ')[1]
        end_time = end_date.split(' ')[1]
        return f"{start_time} - {end_time}"
    except:
        return "Todo el día"