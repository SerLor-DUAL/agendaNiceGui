from nicegui import ui  
from datetime import datetime

def edit_card(event: dict) -> None:
    """ Creates a read-only event card """
    
    # Adapt the event data to the expected format
    start = datetime.fromisoformat(event['start_date'])
    end = datetime.fromisoformat(event['end_date'])

    # Inputs ocultos inicialmente
    title_input = ui.input(value=event['title']).props('outlined').props('dense').classes('w-full hidden')
    desc_input = ui.input(value=event['description']).props('outlined').props('dense').classes('w-full hidden')
    start_input = ui.input(value=start.strftime('%Y-%m-%dT%H:%M')).props('type=datetime-local').classes('w-full hidden')
    end_input = ui.input(value=end.strftime('%Y-%m-%dT%H:%M')).props('type=datetime-local').classes('w-full hidden')

    def hide_edit_event(is_hidden: bool):
        for input in [title_input, desc_input, start_input, end_input]:
            input.classes(remove='hidden') if is_hidden else input.classes(add='hidden')

    def get_values():
        return {
            'title': title_input.value,
            'description': desc_input.value,
            'start_date': start_input.value,
            'end_date': end_input.value,
        }

    return hide_edit_event, get_values