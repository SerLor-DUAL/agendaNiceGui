# frontend/components/diary/events/event_dialog.py

# Import necessary modules
from nicegui import ui      # Import the ui module from nicegui

# frontend/components/diary/events/event_dialog.py

from nicegui import ui
from datetime import datetime


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

    def extract_date_time(iso_or_custom: str):
        """Extrae fecha y hora en formato dd/mm/yyyy y HH:MM desde cadena ISO o personalizada"""
        try:
            if 'T' in iso_or_custom:
                dt = datetime.fromisoformat(iso_or_custom)
                return dt.strftime('%d/%m/%Y'), dt.strftime('%H:%M')
            elif ' ' in iso_or_custom:
                parts = iso_or_custom.split(' ')
                return parts[0], parts[1]
            return '', ''
        except Exception:
            return '', ''

    with ui.dialog() as dialog, ui.card().classes('w-[500px] p-6'):
        
        ui.label(f'{title} - Día {event_data["day"]}').classes('text-xl font-bold mb-6 text-gray-800')

        if action == 'delete':
            ui.label('¿Estás seguro de que quieres eliminar este evento?').classes('text-gray-700 mb-3')

            with ui.card().classes('bg-red-50 border-l-4 border-red-400 p-4 mb-4'):
                ui.label(event_data.get('title', '')).classes('font-semibold text-red-800')
                ui.label(event_data.get('description', '')).classes('text-sm text-red-700')
                ui.label(format_time_range(event_data.get('start_date', ''), event_data.get('end_date', ''))).classes('text-xs text-red-600')

        else:
            # Obtener partes de fechas
            start_date_str, start_time_str = extract_date_time(event_data.get('start_date', ''))
            end_date_str, end_time_str = extract_date_time(event_data.get('end_date', ''))

            title_input = ui.input('Título del evento', value=event_data.get('title', '')).classes('w-full mb-4').props('outlined')
            description_input = ui.textarea('Descripción', value=event_data.get('description', '')).classes('w-full mb-4').props('outlined')

            with ui.row().classes('w-full gap-4 mb-4'):
                with ui.column().classes('flex-1'):
                    ui.label('Fecha y hora de inicio').classes('text-sm font-medium text-gray-700 mb-2')
                    start_date_input = ui.input('Fecha inicio', value=start_date_str).classes('w-full mb-2').props('outlined').tooltip('Formato: dd/mm/aaaa')
                    start_time_input = ui.input('Hora inicio', value=start_time_str).classes('w-full').props('outlined').tooltip('Formato: hh:mm')

                with ui.column().classes('flex-1'):
                    ui.label('Fecha y hora de fin').classes('text-sm font-medium text-gray-700 mb-2')
                    end_date_input = ui.input('Fecha fin', value=end_date_str).classes('w-full mb-2').props('outlined').tooltip('Formato: dd/mm/aaaa')
                    end_time_input = ui.input('Hora fin', value=end_time_str).classes('w-full').props('outlined').tooltip('Formato: hh:mm')

        with ui.row().classes('w-full justify-end gap-3 mt-6'):
            ui.button('Cancelar', on_click=dialog.close).props('flat').classes('text-gray-600 px-4')

            if action == 'delete':
                ui.button(button_text, on_click=lambda: on_delete(event_data)).classes('bg-red-500 text-white hover:bg-red-600 px-6')
            else:
                def handle_action():
                    new_event = {
                        'title': title_input.value,
                        'description': description_input.value,
                        'start_date': f'{start_date_input.value} {start_time_input.value}',
                        'end_date': f'{end_date_input.value} {end_time_input.value}',
                    }
                    on_save(new_event)
                    dialog.close()

                ui.button(button_text, on_click=handle_action).classes(f'bg-{button_color}-500 text-white hover:bg-{button_color}-600 px-6')

    return dialog


def format_time_range(start_date, end_date):
    """Formats time range for display"""
    try:
        # _ is used when the first value is not going to be used.
        _, start_time = datetime.fromisoformat(start_date).strftime('%d/%m/%Y %H:%M').split(' ')
        _, end_time = datetime.fromisoformat(end_date).strftime('%d/%m/%Y %H:%M').split(' ')
        return f"{start_time} - {end_time}"
    except Exception:
        return "Todo el día"
