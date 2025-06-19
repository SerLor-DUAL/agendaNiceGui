# frontend/components/diary/events/event_card.py

# Importing necessary modules
from datetime import datetime
from nicegui import ui

def event_card(event: dict, on_edit: callable = None, on_delete: callable = None, is_monthly: bool = False) -> None:
    """Render an event card"""
    
    card_classes = _get_card_classes(is_monthly)
    
    with ui.card().classes(card_classes):
        with ui.row().classes('w-full items-start justify-between'):
            _render_event_info(event, is_monthly)
            _render_event_actions(event, on_edit, on_delete, is_monthly)


def _get_card_classes(is_monthly: bool) -> str:
    """Get appropriate card classes based on context"""
    
    base = 'w-full mb-3 p-4 border-l-4 transition-colors'
    
    if is_monthly:
        return f'{base} bg-indigo-50 border-indigo-500 hover:bg-indigo-100'
    
    return f'{base} bg-blue-50 border-blue-500 hover:bg-blue-100'


def _render_event_info(event: dict, is_monthly: bool) -> None:
    """Render event information section"""
    
    with ui.column().classes('flex-1 gap-1'):
        title_size = 'text-sm' if is_monthly else 'text-base'
        ui.label(event['title']).classes(f'{title_size} font-semibold text-gray-800')
        
        if event.get('description'):
            desc_size = 'text-xs' if is_monthly else 'text-sm'
            ui.label(event['description']).classes(f'{desc_size} text-gray-600')
        
        time_color = 'text-indigo-600' if is_monthly else 'text-blue-600'
        
        ui.label(_format_time_range(event['start_date'], event['end_date'])) \
            .classes(f'text-xs font-medium {time_color}')


def _render_event_actions(event: dict, on_edit: callable, on_delete: callable, is_monthly: bool) -> None:
    """Render event action buttons"""
    
    if not (on_edit or on_delete):
        return
        
    with ui.row().classes('gap-1 ml-2'):
        
        # Edit
        if on_edit:
            btn_classes = 'text-indigo-600 hover:bg-indigo-200' if is_monthly else 'text-blue-600 hover:bg-blue-200'
            ui.button(icon='edit', on_click=lambda: on_edit(event)) \
                .props('dense round flat size=xs' if is_monthly else 'dense round flat') \
                .classes(btn_classes) \
                .tooltip('Editar evento')
        
        # Delete        
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