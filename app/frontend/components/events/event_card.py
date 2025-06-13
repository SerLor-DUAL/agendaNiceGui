# frontend/routes/calendar.py

# Import necessary modules
from nicegui import ui                                                             # Importing ui from nicegui
from frontend.components.events.read_card import read_event
from frontend.components.events.edit_card import edit_card
# ----------------------------------------------------------------------------------------------------------------------------------------- #


async def create_events_card(event: dict) -> None:
    """ Creates the events page """
    # state to control visibility of inputs
    is_editing = False

    with ui.card().classes("w-full p-4 bg-white shadow rounded"):

        show_read = read_event(event)
        show_edit, get_edit_values = edit_card(event)

        edit_btn = ui.button('✏️ Editar')
        save_btn = ui.button('💾 Guardar').classes('hidden')
        cancel_btn = ui.button('Cancelar').classes('hidden')

        def toggle_edit_mode():
            nonlocal is_editing
            is_editing = not is_editing

            show_read(not is_editing)
            show_edit(is_editing)

            edit_btn.visible = not is_editing
            save_btn.classes(remove='hidden') if is_editing else save_btn.classes(add='hidden')
            cancel_btn.classes(remove='hidden') if is_editing else cancel_btn.classes(add='hidden')
        def save_edits():
            nonlocal is_editing
            is_editing = False

            values = get_edit_values()
            print('Valores editados:', values)

            # TODO: 
            toggle_edit_mode()

        edit_btn.on('click', toggle_edit_mode)
        save_btn.on('click', save_edits)
        cancel_btn.on('click', toggle_edit_mode)