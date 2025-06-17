# frontend/components/diary/diary_card.py

# Import necessary modules
import calendar
from nicegui import ui
from datetime import datetime
from frontend.components.diary.diary_day_card import create_diary_day_card
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Global calendar state
calendar_state = {
    'year': datetime.now().year,
    'month': datetime.now().month,
    'selected_day': datetime.now().day,
    'view_mode': 'calendar'                 # 'calendar' or 'monthly'
}

# Mock events data - replace with your actual data source
events_data = {
    1: [
        {
            "titulo": "Reunión de trabajo",
            "descripcion": "Reunión semanal del equipo de desarrollo",
            "start_date": "01/06/2025 09:00",
            "end_date": "01/06/2025 10:30"
        },
        {
            "titulo": "Cita médica",
            "descripcion": "Revisión médica anual",
            "start_date": "01/06/2025 15:00",
            "end_date": "01/06/2025 16:00"
        }
    ],
    5: [
        {
            "titulo": "Cumpleaños de María",
            "descripcion": "Celebración en el restaurante italiano",
            "start_date": "05/06/2025 20:00",
            "end_date": "05/06/2025 23:30"
        }
    ],
    17: [
        {
            "titulo": "Dentista",
            "descripcion": "Limpieza dental rutinaria",
            "start_date": "17/06/2025 10:00",
            "end_date": "17/06/2025 11:00"
        },
        {
            "titulo": "Compras",
            "descripcion": "Compras semanales en el supermercado",
            "start_date": "17/06/2025 16:00",
            "end_date": "17/06/2025 17:30"
        },
        {
            "titulo": "Gimnasio",
            "descripcion": "Entrenamiento de piernas",
            "start_date": "17/06/2025 18:00",
            "end_date": "17/06/2025 19:30"
        },
        {
            "titulo": "Cena con amigos",
            "descripcion": "Cena en el nuevo restaurante asiático",
            "start_date": "17/06/2025 21:00",
            "end_date": "17/06/2025 23:00"
        }
    ]
}

# Function to create a calendar card
def diary_card():
    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # METHODS #
    
        # ----------------------------------------------------------------------------------------------------------------------------------------- #
        # FORMAT #
    
    def get_events_for_day(day):
        """Get events for a specific day"""
        return events_data.get(day, [])
    
    def get_all_events_for_month():
        """Get all events for the current month"""
        month_events = []
        for day, events in events_data.items():
            for event in events:
                event_with_day = event.copy()
                event_with_day['day'] = day
                month_events.append(event_with_day)
        return sorted(month_events, key=lambda x: (x['day'], x['start_date']))
    
    def format_time_range(start_date, end_date):
        """Format time range for display"""
        try:
            start_time = start_date.split(' ')[1]
            end_time = end_date.split(' ')[1]
            return f"{start_time} - {end_time}"
        except:
            return "Todo el día"
    
    def format_date_title(day, month, year):
        """Format date for title display"""
        return f"{day:02d}-{month:02d}-{year}"

        # ----------------------------------------------------------------------------------------------------------------------------------------- #
        # INTERACTION #

    def update_events_panel(events_container):
        """Update the events panel for the selected day or month view"""
        events_container.clear()
        
        # Events container
        with events_container:
            
            # Mode calendar
            if calendar_state['view_mode'] == 'calendar':
                
                selected_day = calendar_state['selected_day']
                events = get_events_for_day(selected_day)
                
                # Events header
                date_title = format_date_title(selected_day, calendar_state['month'], calendar_state['year'])
                with ui.row().classes('w-full items-center justify-between mb-4'):
                    ui.label(f'Eventos de {date_title}').classes('text-lg font-bold text-gray-800')
                    ui.button(icon='add', color='green', on_click=lambda: show_event_dialog('create', selected_day)) \
                        .props('dense round') \
                        .classes('bg-green-500 hover:bg-green-600') \
                        .tooltip('Agregar evento')
                
                # Scrollable events container
                with ui.scroll_area().classes('h-[600px] w-full hide-scroll'):
                    ui.run_javascript("""
                        document.querySelectorAll('.hide-scroll .q-scrollarea__thumb').forEach(el => {
                            el.style.width = '0px';
                            el.style.height = '0px';
                            el.style.opacity = '0';
                            el.style.pointerEvents = 'none';
                        });
                    """)

                    # Events list
                    if events:
                        for i, event in enumerate(events):
                            with ui.card().classes('w-full mb-3 p-4 bg-blue-50 border-l-4 border-blue-500 hover:bg-blue-100 transition-colors'):
                                with ui.row().classes('w-full items-start justify-between'):
                                    with ui.column().classes('flex-1 gap-1'):
                                        ui.label(event['titulo']).classes('text-base font-semibold text-gray-800')
                                        if event.get('descripcion'):
                                            ui.label(event['descripcion']).classes('text-sm text-gray-600')
                                        ui.label(format_time_range(event['start_date'], event['end_date'])).classes('text-xs text-blue-600 font-medium')
                                    
                                    with ui.row().classes('gap-1 ml-2'):
                                        ui.button(icon='edit', on_click=lambda idx=i: show_event_dialog('edit', selected_day, idx)) \
                                            .props('dense round flat') \
                                            .classes('text-blue-600 hover:bg-blue-200') \
                                            .tooltip('Editar evento')
                                        ui.button(icon='delete', on_click=lambda idx=i: show_event_dialog('delete', selected_day, idx)) \
                                            .props('dense round flat') \
                                            .classes('text-red-600 hover:bg-red-200') \
                                            .tooltip('Eliminar evento')
                    
                    # No events message
                    else:
                        with ui.column().classes('w-full items-center py-8 text-center'):
                            ui.icon('event_busy', size='48px').classes('text-gray-300 mb-2')
                            ui.label('No hay eventos programados').classes('text-gray-500 font-medium')
                            ui.label('Haz clic en "+" para agregar uno').classes('text-gray-400 text-sm')
            
            # TODO: Mode monthly events (IMPROVE VISUALIZATION)
            else:
                
                month_events = get_all_events_for_month()
                month_name = calendar.month_name[calendar_state['month']].capitalize()
                year = calendar_state['year']
                
                # Monthly events header
                ui.label(f'Eventos de {month_name} {year}').classes('text-lg font-bold text-gray-800 mb-4')
                
                # TODO: Scrollable monthly events container / CHANGE FOR A CONTAINER
                with ui.scroll_area().classes('h-[600px] w-full'):
                    if month_events:
                        current_day = None
                        for event in month_events:
                            # Day separator
                            if current_day != event['day']:
                                current_day = event['day']
                                if current_day != month_events[0]['day']:  # Add spacing except for first day
                                    ui.separator().classes('my-3')
                                ui.label(f'Día {current_day:02d}').classes('text-sm font-bold text-gray-700 mb-2 mt-3')
                            
                            # Event card
                            with ui.card().classes('w-full mb-2 p-3 bg-indigo-50 border-l-4 border-indigo-500 hover:bg-indigo-100 transition-colors'):
                                with ui.row().classes('w-full items-start justify-between'):
                                    with ui.column().classes('flex-1 gap-1'):
                                        ui.label(event['titulo']).classes('text-sm font-semibold text-gray-800')
                                        if event.get('descripcion'):
                                            ui.label(event['descripcion']).classes('text-xs text-gray-600')
                                        ui.label(format_time_range(event['start_date'], event['end_date'])).classes('text-xs text-indigo-600 font-medium')
                                    
                                    with ui.row().classes('gap-1 ml-2'):
                                        ui.button(icon='edit', on_click=lambda day=event['day']: select_day_and_edit(day)) \
                                            .props('dense round flat size=xs') \
                                            .classes('text-indigo-600 hover:bg-indigo-200') \
                                            .tooltip('Editar evento')
                    else:
                        # No events message
                        with ui.column().classes('w-full items-center py-8 text-center'):
                            ui.icon('event_busy', size='48px').classes('text-gray-300 mb-2')
                            ui.label('No hay eventos este mes').classes('text-gray-500 font-medium')

    def select_day_and_edit(day):
        """Switch to calendar view and select specific day"""
        
        calendar_state['selected_day'] = day
        calendar_state['view_mode'] = 'calendar'
        update_diary(calendar_container, date_label)
        update_events_panel(events_container)
        update_view_button(view_button)

    def show_event_dialog(action, day, event_index=None):
        """Show dialog for event management"""
        
        # Get events for selected day
        events = get_events_for_day(day)
        
        # Create
        if action == 'create':
            title = f'Agregar evento - Día {day}'
            button_text = 'Crear evento'
            button_color = 'green'
            event_data = {
                'titulo': '',
                'descripcion': '',
                'start_date': f'{day:02d}/{calendar_state["month"]:02d}/{calendar_state["year"]} 09:00',
                'end_date': f'{day:02d}/{calendar_state["month"]:02d}/{calendar_state["year"]} 10:00'
            }
        
        # Update   
        elif action == 'edit':
            title = f'Editar evento - Día {day}'
            button_text = 'Guardar cambios'
            button_color = 'blue'
            event_data = events[event_index] if event_index < len(events) else {}
        
        # Delete    
        else:
            title = f'Eliminar evento - Día {day}'
            button_text = 'Eliminar'
            button_color = 'red'
            event_data = events[event_index] if event_index < len(events) else {}

        # Modal dialog for actions related to an event
        with ui.dialog() as dialog, ui.card().classes('w-[500px] p-6'):
            
            # Modal title
            ui.label(title).classes('text-xl font-bold mb-6 text-gray-800')
            
            # Delete confirmation
            if action == 'delete':
                
                # Description
                ui.label('¿Estás seguro de que quieres eliminar este evento?').classes('text-gray-700 mb-3')
                with ui.card().classes('bg-red-50 border-l-4 border-red-400 p-4 mb-4'):
                    ui.label(event_data.get('titulo', '')).classes('font-semibold text-red-800')
                    ui.label(event_data.get('descripcion', '')).classes('text-sm text-red-700')
                    ui.label(format_time_range(event_data.get('start_date', ''), event_data.get('end_date', ''))).classes('text-xs text-red-600')
            else:
                # Form fields
                titulo_input = ui.input('Título del evento', value=event_data.get('titulo', '')) \
                    .classes('w-full mb-4').props('outlined')
                
                descripcion_input = ui.textarea('Descripción', value=event_data.get('descripcion', '')) \
                    .classes('w-full mb-4').props('outlined')
                
                # Date and time inputs
                with ui.row().classes('w-full gap-4 mb-4'):
                    with ui.column().classes('flex-1'):
                        ui.label('Fecha y hora de inicio').classes('text-sm font-medium text-gray-700 mb-2')
                        start_date_input = ui.input('Fecha inicio', value=event_data.get('start_date', '').split(' ')[0] if event_data.get('start_date') else '') \
                            .classes('w-full mb-2').props('outlined').tooltip('Formato: dd/mm/aaaa')
                        start_time_input = ui.input('Hora inicio', value=event_data.get('start_date', '').split(' ')[1] if event_data.get('start_date') else '') \
                            .classes('w-full').props('outlined').tooltip('Formato: hh:mm')
                    
                    with ui.column().classes('flex-1'):
                        ui.label('Fecha y hora de fin').classes('text-sm font-medium text-gray-700 mb-2')
                        end_date_input = ui.input('Fecha fin', value=event_data.get('end_date', '').split(' ')[0] if event_data.get('end_date') else '') \
                            .classes('w-full mb-2').props('outlined').tooltip('Formato: dd/mm/aaaa')
                        end_time_input = ui.input('Hora fin', value=event_data.get('end_date', '').split(' ')[1] if event_data.get('end_date') else '') \
                            .classes('w-full').props('outlined').tooltip('Formato: hh:mm')
            
            with ui.row().classes('w-full justify-end gap-3 mt-6'):
                ui.button('Cancelar', on_click=dialog.close).props('flat').classes('text-gray-600 px-4')
                
                def handle_action():
                    try:
                        if action == 'create':
                            new_event = {
                                'titulo': titulo_input.value,
                                'descripcion': descripcion_input.value,
                                'start_date': f'{start_date_input.value} {start_time_input.value}',
                                'end_date': f'{end_date_input.value} {end_time_input.value}'
                            }
                            if day not in events_data:
                                events_data[day] = []
                            events_data[day].append(new_event)
                            ui.notify(f'Evento "{new_event["titulo"]}" creado correctamente', type='positive')
                            
                        elif action == 'edit':
                            updated_event = {
                                'titulo': titulo_input.value,
                                'descripcion': descripcion_input.value,
                                'start_date': f'{start_date_input.value} {start_time_input.value}',
                                'end_date': f'{end_date_input.value} {end_time_input.value}'
                            }
                            events_data[day][event_index] = updated_event
                            ui.notify(f'Evento "{updated_event["titulo"]}" actualizado correctamente', type='positive')
                            
                        else:  # delete
                            deleted_title = events_data[day][event_index]['titulo']
                            events_data[day].pop(event_index)
                            if not events_data[day]:
                                del events_data[day]
                            ui.notify(f'Evento "{deleted_title}" eliminado correctamente', type='warning')
                        
                        dialog.close()
                        update_diary(calendar_container, date_label)
                        update_events_panel(events_container)
                        
                    except Exception as e:
                        ui.notify(f'Error al procesar el evento: {str(e)}', type='negative')
                
                ui.button(button_text, on_click=handle_action) \
                    .classes(f'bg-{button_color}-500 text-white hover:bg-{button_color}-600 px-6')
        
        dialog.open()

    def update_diary(container, date_label):
        """ Updates the calendar """
        
        # Clear the container
        container.clear()
        
        # Get the current month and year from the calendar state
        year = calendar_state['year']
        month = calendar_state['month']
        
        # Get the selected day from the calendar state
        selected_day = calendar_state['selected_day']
        
        # Create a calendar object
        cal = calendar.Calendar(firstweekday=0)
        
        # Get the days of the month
        month_days = cal.monthdayscalendar(year, month)
        
        # Assign the weekdays naming
        days_of_week = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        # Get the current date
        today = datetime.today()
        
        # When a day is selected    
        def on_select(day):
            
            # Update the calendar state
            calendar_state['selected_day'] = day
            if calendar_state['view_mode'] == 'monthly':
                calendar_state['view_mode'] = 'calendar'
                
                # Update the view mode of the view button
                update_view_button(view_button)
                
            # Updates the diary and events panel
            update_diary(container, date_label)
            update_events_panel(events_container)
        
        # Calendar container
        with container:
            
            # In calendar mode
            if calendar_state['view_mode'] == 'calendar':
                
                # Creates the weekdays header
                with ui.grid().classes('w-full px-2').style('grid-template-columns:repeat(7, minmax(0, 1fr));'):
                    for day in days_of_week:
                        ui.label(day).classes('text-center font-medium text-gray-500 text-lg')

                # Creates the grid for days
                with ui.grid().classes('w-full p-2 gap-3').style('grid-template-columns: repeat(7, minmax(0, 1fr)); grid-auto-rows: 75px;'):
                    for i in range(6):
                        week = month_days[i] if i < len(month_days) else [0]*7
                        for day in week:
                            is_today = (day == today.day and month == today.month and year == today.year)
                            is_selected = (day == selected_day)
                            
                            # If the day is 0, it is a placeholder
                            if day == 0:
                                ui.element('div').classes('bg-gray-100 shadow-lg rounded-lg')
                                
                            # If not then, creates a day card
                            else:
                                event_count = len(get_events_for_day(day))
                                create_diary_day_card(day, event_count, is_today, is_selected, on_select)
            
            # In monthly mode
            else:
                with ui.column().classes('w-full'):
                    ui.label('Vista de lista mensual').classes('text-center text-gray-500 text-lg font-medium mb-4')
                    ui.label('Los eventos se muestran en el panel lateral →').classes('text-center text-gray-400 text-sm')
        
        date_label.set_text(f"{calendar.month_name[month].capitalize()} {year}")

    def change_month(offset: int, container, date_label):
        """ Changes the month and updates the calendar """
        
        #Calculate month and year
        m = calendar_state['month'] + offset
        y = calendar_state['year']
        
        if m > 12:
            m = 1
            y += 1
        elif m < 1:
            m = 12
            y -= 1
        
        # Change state
        calendar_state['month'] = m
        calendar_state['year'] = y
        
        # Updates UI
        update_diary(container, date_label)
        update_events_panel(events_container)
        
    def go_to_today(container, date_label):
        """ Jumps to the current month/year """
        
        # Change state and sets to today
        today = datetime.today()
        calendar_state['year'] = today.year
        calendar_state['month'] = today.month
        calendar_state['selected_day'] = today.day
        
        # Updates UI
        update_diary(container, date_label)
        update_events_panel(events_container)
    
    def toggle_view_mode(container, date_label, button):
        """ Toggle between calendar and monthly view """
        
        # Change state
        if calendar_state['view_mode'] == 'calendar':
            calendar_state['view_mode'] = 'monthly'
        else:
            calendar_state['view_mode'] = 'calendar'
        
        # Updates UI
        update_diary(container, date_label)
        update_events_panel(events_container)
        update_view_button(button)
    
    def update_view_button(button):
        """ Update view button text and icon """
        
        # Change state
        if calendar_state['view_mode'] == 'calendar':
            button.set_text('Vista mensual')
            button.props('icon=calendar_view_month')
        else:
            button.set_text('Vista calendario')
            button.props('icon=calendar_view_day')

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # UI #
    
    # Principal Container
    with ui.row().classes('h-fit w-full justify-center p-4'):
        
        # Main card
        with ui.card().classes('w-full max-w-7xl bg-white rounded-xl shadow-lg overflow-hidden'):
            
            # Calendar controls
            with ui.row().classes('w-full items-center justify-between px-6 py-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-b'):
                
                # Month navigation
                with ui.row().classes('items-center gap-3'):
                    ui.button(icon='chevron_left', on_click=lambda: change_month(-1, calendar_container, date_label)) \
                        .props('dense round') \
                        .classes('bg-blue text-blue-600 hover:bg-blue-50 shadow-sm border')
                    
                    date_label = ui.label().classes('text-2xl font-bold text-gray-800 min-w-[200px] text-center')
                    
                    ui.button(icon='chevron_right', on_click=lambda: change_month(1, calendar_container, date_label)) \
                        .props('dense round') \
                        .classes('bg-blue text-blue-600 hover:bg-blue-50 shadow-sm border')
                
                # Action buttons
                with ui.row().classes('gap-3'):
                    ui.button('Hoy', icon='today', on_click=lambda: go_to_today(calendar_container, date_label)) \
                        .classes('bg-blue-500 text-white hover:bg-blue-600 px-4 py-2 shadow-sm')
                    view_button = ui.button('Vista mensual', icon='calendar_view_month', on_click=lambda: toggle_view_mode(calendar_container, date_label, view_button)) \
                        .props('outline') \
                        .classes('text-blue-600 border-blue-600 hover:bg-blue-50 px-4 py-2')
            
            # Content area with calendar and events panel
            with ui.row().classes('w-full').style('height: 600px'):
                
                # Calendar section (left side)
                with ui.column().classes('flex-1 p-6'):
                    calendar_container = ui.column().classes('w-full')
                
                # Events panel (right side)
                with ui.column().classes('w-80 bg-gray-50 border-l p-6').style('height: 600px; overflow: hidden;'):
                    events_container = ui.column().classes('w-full h-full')
                    
            # Initialize
            update_diary(calendar_container, date_label)
            update_events_panel(events_container)