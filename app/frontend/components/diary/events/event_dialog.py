# frontend/components/diary/events/event_dialog.py

# Importing necessary modules
from nicegui import ui
from datetime import datetime
from frontend.services.event_services import front_event_service as es
import asyncio

def show_event_dialog(action: str, event_data: dict, on_save: callable, on_delete: callable = None) -> ui.dialog:
    """Show dialog for event CRUD operations"""
    
    dialog = ui.dialog()
    title, button_text, button_color = _get_dialog_config(action)
    
    with dialog, ui.card().classes('w-[500px] p-6 flex flex-row'):
        ui.label(f'{title} - Día {event_data["day"]}').classes('text-xl font-bold mb-6')
        
        # Render content based on action type
        if action == 'delete':
            _render_delete_confirmation(event_data)
            _render_delete_actions(dialog, event_data, on_delete)
        else:
            inputs = _render_event_form(event_data)
            _render_form_actions(dialog, action, button_text, button_color, inputs, event_data, on_save)

    return dialog


def _get_dialog_config(action: str) -> tuple:
    """Get dialog configuration based on action type"""
    
    titles = {'create': 'Agregar evento', 'edit': 'Editar evento', 'delete': 'Eliminar evento'}
    buttons = {'create': 'Crear evento', 'edit': 'Guardar cambios', 'delete': 'Eliminar'}
    colors = {'create': 'green', 'edit': 'blue', 'delete': 'red'}
    
    # Returns the title, button text, and color based on the action
    return titles[action], buttons[action], colors[action]


def _render_delete_confirmation(event_data: dict) -> None:
    """Render delete confirmation content"""
    
    ui.label('¿Estás seguro de que quieres eliminar este evento?').classes('text-gray-700 mb-3')
    with ui.card().classes('bg-red-50 border-l-4 border-red-400 p-4 mb-4 min-w-[75%] self-center'):
        title = event_data.get('title', 'Evento sin título')
        ui.label(title).classes('font-semibold text-red-800 truncate w-full') # Usamos Truncate de Tailwind para truncar el texto
        description = event_data.get('description')
        if description:
            ui.label(description).classes('text-sm text-red-700 truncate w-full') # Usamos Truncate de Tailwind para truncar el texto

        # Formatted time range display
        ui.label(_format_time_range(event_data.get('start_date', ''), event_data.get('end_date', ''))).classes('text-xs text-red-600')

def _render_event_form(event_data: dict) -> dict:
    """Render event form inputs and return references"""
    
    start_date, start_time = _extract_date_time(event_data.get('start_date', ''))
    end_date, end_time = _extract_date_time(event_data.get('end_date', ''))
    
    # Initialize input fields with existing event data or defaults
    inputs = {
        'title': ui.input('Título', value=event_data.get('title', '')).classes('w-full mb-4').props('outlined').props('maxlength=100'),
        'description': ui.textarea('Descripción', value=event_data.get('description', '')).classes('w-full mb-4').props('outlined').props('maxlength=500'),
        'start_date_title': ui.label('Fecha y hora de inicio').classes('text-sm font-medium text-gray-700 w-[48%] text-center'),
        'end_date_title': ui.label('Fecha y hora de fin').classes('text-sm font-medium text-gray-700 w-[48%] text-center'),
        'start_date': ui.input('Fecha inicio', value=start_date).classes('w-[48%] mb-2').props('outlined'),
        'end_date': ui.input('Fecha fin', value=end_date).classes('w-[48%]').props('outlined'),
        'start_time': ui.input('Hora inicio', value=start_time).classes('w-[48%] mb-2').props('outlined'),
        'end_time': ui.input('Hora fin', value=end_time).classes('w-[48%]').props('outlined'),
    }
    
    return inputs

def _render_form_actions(dialog: ui.dialog, action: str, button_text: str, button_color: str, inputs: dict, event_data: dict, on_save: callable) -> None:
    """Render form action buttons"""
    
    with ui.row().classes('w-full justify-end gap-3 mt-6'):
        ui.button('Cancelar', on_click=dialog.close).props('flat').classes('text-gray-600 px-4')
        ui.button(button_text, on_click=lambda: _handle_form_action(action, inputs, event_data, on_save, dialog)) \
            .classes(f'bg-{button_color}-500 text-white hover:bg-{button_color}-600 px-6')


def _render_delete_actions(dialog: ui.dialog, event_data: dict, on_delete: callable) -> None:
    """Render delete action buttons"""
    with ui.row().classes('w-full justify-end gap-3 mt-6'):
        ui.button('Cancelar', on_click=dialog.close).props('flat').classes('text-gray-600 px-4')
        ui.button('Eliminar', on_click=lambda: _handle_delete(event_data, on_delete, dialog)) \
            .classes('bg-red-500 text-white hover:bg-red-600 px-6')


async def _handle_form_action(action: str, inputs: dict, event_data: dict, on_save: callable, dialog: ui.dialog) -> None:
    """Handle form submission for create/edit actions"""
    
    # Validate operations for form submit
    try:
        
        # Validar campos requeridos
        if not inputs['title'].value.strip():
            ui.notify('El título es requerido', color='negative')
            return

        # Construir objeto del evento
        new_event = {
                        'title': inputs['title'].value,
                        'description': inputs['description'].value,
                        'start_date': _combine_date_time_to_iso(inputs['start_date'].value, inputs['start_time'].value),
                        'end_date': _combine_date_time_to_iso(inputs['end_date'].value, inputs['end_time'].value),
                    }
        
        # Ejecutar operación en backend
        result = None
        
        if action == 'create':
            result = await es.create_event(new_event)
            if not result or 'id' not in result:
                raise ValueError("El evento no se creó correctamente")
        else:
            event_id = event_data['id']
            print("Updating event with ID:", new_event)
            result = await es.update_event(event_id, new_event)
            if not result:
                raise ValueError("El evento no se actualizó correctamente")
            result['id'] = event_id
        
        await on_save(result)
        
        dialog.close()

    # Handle any exceptions that occur during the operation
    except Exception as e:
        ui.notify(f'Error: {str(e)}', color='negative')


async def _handle_delete(event_data: dict, on_delete: callable, dialog: ui.dialog) -> None:
    """Handle event deletion"""
    
    # Validate operation for form submit
    try:
        
        if 'id' not in event_data:
            raise ValueError("ID de evento no encontrado")
        
        # Delete
        await es.delete_event(event_data["id"])
        await on_delete(event_data)
        
        # Close dialog after successful operation 
        dialog.close()
        
    # Handle any exceptions that occur during the operation
    except Exception as e:
        ui.notify(f'Error: {str(e)}', color='negative')

# -------------------------------------------------------------------------------------------------------- #
# TIME AND DATE FUNCTIONS #

def _extract_date_time(date_str: str) -> tuple:
    """Extract date and time components from string"""
    
    try:
        
        # ISO format
        if 'T' in date_str:  
            dt = datetime.fromisoformat(date_str)
            return dt.strftime('%d/%m/%Y'), dt.strftime('%H:%M')
        
        # Custom format
        elif ' ' in date_str:  
            date_part, time_part = date_str.split(' ')
            return date_part, time_part
        
    # Default case
    except Exception:
        return '', ''

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
    
    
def _combine_date_time_to_iso(date_str: str, time_str: str) -> str:
    """Combine date and time strings into ISO  datetime string"""
    try:
        dt = datetime.strptime(f'{date_str} {time_str}', '%d/%m/%Y %H:%M')
        return dt.isoformat()
    except Exception:
        return ''