# frontend/components/diary/events/event_card.py

# Importing necessary modules
from datetime import datetime
from nicegui import ui

def event_card(event: dict, on_edit: callable = None, on_delete: callable = None, is_monthly: bool = False) -> None:
    """Render an event card"""
    
    card_classes = _get_card_classes(is_monthly)
    
    with ui.card().classes(card_classes):
        # Column with 100% width inside the card
        with ui.column().classes('items-start justify-between').style('width: 100%;'):
            _render_event_info(event, on_edit, on_delete, is_monthly)

def _get_card_classes(is_monthly: bool) -> str:
    base = 'mb-3 p-4 border-l-4 transition-all duration-300 w-full'
    if is_monthly:
        return f'{base} bg-white border-blue-400 hover:bg-blue-50 hover:border-blue-600 shadow-md hover:shadow-lg max-w-5xl'
    return f'{base} bg-blue-50 border-blue-500 hover:bg-blue-100 max-w-sm'

def _render_event_info(event: dict, on_edit: callable, on_delete: callable, is_monthly: bool) -> None:
    """Adds event info to the card with buttons always vertically centered on the right, never displaced below.
        Text will not grow the card; overflow is ellipsis."""

    title_size = 'text-sm' if is_monthly else 'text-base'
    desc_size = 'text-xs' if is_monthly else 'text-sm'
    time_color = 'text-blue-600' if is_monthly else 'text-blue-600'

    # Use grid to keep buttons always at the right, regardless of text length
    with ui.element('div').classes('w-full grid grid-cols-[1fr_auto] items-center gap-2'):
        
        # Left: Event info
        with ui.column().classes('max-w-full overflow-hidden'):
            
            # Title
            ui.label(event['title']).classes(f'{title_size} font-semibold text-gray-800 overflow-hidden') \
                .style(
                    'max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; word-break: normal;'
                ) \
                .tooltip(event['title'][:20 if is_monthly else 30] + '...')

            # Description
            if event.get('description'):
                description = event['description'][:60 if is_monthly else 70]
                if len(event['description']) > (60 if is_monthly else 70):
                    description += '...'
                ui.label(description).classes(f'{desc_size} text-gray-600 mt-1 overflow-hidden') \
                    .style(
                        'max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; '
                        'word-break: break-word; overflow-wrap: break-word;'
                    ) \
                    .tooltip(event['description'][:40 if is_monthly else 50] + '...')

            # Time
            ui.label(_format_time_range(event['start_date'], event['end_date'])) \
                .classes(f'text-xs font-medium {time_color} mt-1 overflow-hidden') \
                .style('max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;')

        # Right: Buttons
        with ui.column().classes('items-center justify-center min-w-[10%]'):
            if on_edit:
                btn_classes = 'text-blue-600 hover:bg-blue-200'
                ui.button(icon='edit', on_click=lambda: on_edit(event)) \
                    .props('dense round flat size=xs' if is_monthly else 'dense round flat') \
                    .classes(btn_classes) \
                    .tooltip('Editar evento')
            if on_delete:
                ui.button(icon='delete', on_click=lambda: on_delete(event)) \
                    .props('dense round flat size=xs' if is_monthly else 'dense round flat') \
                    .classes('text-red-600 hover:bg-red-200') \
                    .tooltip('Eliminar evento')

# -------------------------------------------------------------------------------------------------------- #
# TIME AND DATE FUNCTIONS #

def _format_time_range(start_date: str, end_date: str) -> str:
    """Format time range for display"""
    
    # Try to convert to datetime and format
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        return f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
    
    # If conversion fails, return a default message
    except Exception:
        return "Todo el día"