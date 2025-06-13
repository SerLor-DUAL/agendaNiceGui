from nicegui import ui  
from datetime import datetime

def read_event(event: dict) -> None:
    """ Creates a read-only event card """
    
    # Adapt the event data to the expected format
    start = datetime.fromisoformat(event['start_date'])
    end = datetime.fromisoformat(event['end_date'])

    # Labels
    title_label = ui.label(event['title']).classes('text-xl font-semibold')
    desc_label = ui.label(event['description']).classes('text-gray-700')
    start_label = ui.label(f"🕒 Desde: {start.strftime('%d %b %Y, %H:%M')}").classes('text-sm text-gray-500')
    end_label = ui.label(f"⏱️ Hasta: {end.strftime('%d %b %Y, %H:%M')}").classes('text-sm text-gray-500')

    def hide_read_event(isHidden: bool):
        # Mostrar u ocultar elementos
        title_label.visible = isHidden
        desc_label.visible = isHidden
        start_label.visible = isHidden
        end_label.visible = isHidden
    return hide_read_event