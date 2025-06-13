# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                             # Importing ui from nicegui
from datetime import datetime                                                      # Importing datetime for date formatting
# ----------------------------------------------------------------------------------------------------------------------------------------- #


async def create_events_card(event: dict) -> None:
    """ Creates the events page """

    # Adapt the event data to the expected format
    start = datetime.fromisoformat(event['start_date'])
    end = datetime.fromisoformat(event['end_date'])

    # state to control visibility of inputs
    is_editing = False

     # Labels
    title_label = ui.label(event['title']).classes('text-xl font-semibold')
    desc_label = ui.label(event['description']).classes('text-gray-700')
    start_label = ui.label(f"🕒 Desde: {start.strftime('%d %b %Y, %H:%M')}").classes('text-sm text-gray-500')
    end_label = ui.label(f"⏱️ Hasta: {end.strftime('%d %b %Y, %H:%M')}").classes('text-sm text-gray-500')

    # Inputs ocultos inicialmente
    title_input = ui.input(value=event['title']).props('outlined').props('dense').classes('w-full hidden')
    desc_input = ui.input(value=event['description']).props('outlined').props('dense').classes('w-full hidden')
    start_input = ui.input(value=start.strftime('%Y-%m-%dT%H:%M')).props('type=datetime-local').classes('w-full hidden')
    end_input = ui.input(value=end.strftime('%Y-%m-%dT%H:%M')).props('type=datetime-local').classes('w-full hidden')

    # Botones
    edit_btn = ui.button('✏️ Editar')
    save_btn = ui.button('💾 Guardar').classes('hidden')

    def toggle_edit_mode():
        nonlocal is_editing
        is_editing = not is_editing

        # Mostrar u ocultar elementos
        title_label.visible = not is_editing
        desc_label.visible = not is_editing
        start_label.visible = not is_editing
        end_label.visible = not is_editing

        title_input.classes(remove='hidden') if is_editing else title_input.classes(add='hidden')
        desc_input.classes(remove='hidden') if is_editing else desc_input.classes(add='hidden')
        start_input.classes(remove='hidden') if is_editing else start_input.classes(add='hidden')
        end_input.classes(remove='hidden') if is_editing else end_input.classes(add='hidden')
        save_btn.classes(remove='hidden') if is_editing else end_input.classes(add='hidden')
        edit_btn.visible = not is_editing
        # save_btn.visible = is_editing

    def save_edits():
        nonlocal is_editing
        is_editing = False

        # Actualizar valores
        title_label.text = title_input.value
        desc_label.text = desc_input.value
        start_label.text = f"🕒 Desde: {datetime.fromisoformat(start_input.value).strftime('%d %b %Y, %H:%M')}"
        end_label.text = f"⏱️ Hasta: {datetime.fromisoformat(end_input.value).strftime('%d %b %Y, %H:%M')}"

        toggle_edit_mode()

    edit_btn.on('click', toggle_edit_mode)
    save_btn.on('click', save_edits)