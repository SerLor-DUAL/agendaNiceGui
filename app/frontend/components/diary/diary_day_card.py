# frontend/components/diary/diary_day_card.py
from nicegui import ui

def create_diary_day_card(day: int, event_count: int, is_today: bool, is_selected: bool, on_select: callable) -> None:
    """Create a day card for calendar view"""
    
    card_classes = _get_card_classes(is_today, is_selected)
    text_classes = _get_text_classes(is_today, is_selected)
    
    with ui.card().classes(f'w-full h-full p-1.5 cursor-pointer rounded-lg {card_classes}') as card:
        card.on('click', lambda: on_select(day))
        
        with ui.column().classes('w-full h-full justify-between'):
            ui.label(str(day)).classes(f'text-base font-semibold {text_classes}')
            
            # Solo mostrar badge si hay eventos
            if event_count > 0:
                ui.badge(str(event_count)).classes(
                    'text-xs font-bold bg-blue-500 text-white px-1.5 py-0.5 shadow-sm min-w-[24px]'
                ).style('opacity: 0.9;')


def _get_card_classes(is_today: bool, is_selected: bool) -> str:
    """Determine card styling classes"""
    
    if is_today and is_selected:
        return 'bg-gradient-to-br from-sky-50 to-sky-100 border-2 border-sky-500 shadow-md'
    elif is_today:
        return 'bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-500 shadow-md'
    elif is_selected:
        return 'bg-gradient-to-br from-sky-50 to-sky-100 border-2 border-sky-400 shadow-md'
    
    # If not today or selected, use default styling
    return 'bg-white border-2 border-gray-100 shadow-sm hover:shadow-md hover:bg-blue-50'


def _get_text_classes(is_today: bool, is_selected: bool) -> str:
    """Determine text styling classes"""
    
    if is_today and is_selected:
        return 'text-sky-800'
    elif is_today:
        return 'text-blue-700'
    elif is_selected:
        return 'text-sky-700'
    
    # If not today or selected, use default styling
    return 'text-gray-700'