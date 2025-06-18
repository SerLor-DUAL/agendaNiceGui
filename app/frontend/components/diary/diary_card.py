# frontend/components/diary/diary_card.py

# Importing necessary modules
import calendar                                                                         # Importing for calendar operations
import locale                                                                           # Importing for locale operations
from nicegui import ui                                                                  # Importing for GUI operations
from datetime import datetime                                                           # Importing for date and time operations
from frontend.components.diary.calendar.calendar_mode import calendar_mode              # Importing for calendar mode
from frontend.components.diary.calendar.monthly_mode import monthly_mode                # Importing for monthly mode
from frontend.components.diary.events.events_list import events_list                    # Importing for events list
from frontend.components.diary.events.events_list import event_card                     # Importing for event card
from frontend.components.diary.events.event_dialog import show_event_dialog             # Importing for event dialog

# Setting the locale to Spanish
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class DiaryCard:
    
    def  __init__(self, event_data: dict):
        
        # Calendar state
        self.calendar_state = {
                                'year': datetime.now().year,
                                'month': datetime.now().month,
                                'selected_day': datetime.now().day,
                                'view_mode': 'calendar'
                            }
        
        # UI elements
        self.date_label = None
        self.calendar_container = None
        self.events_container = None
        self.view_button = None
        
        self.events_data = event_data
        # # Events data
        # self.events_data = {
        #     1: [
        #         {"titulo": "Reunión de trabajo", "descripcion": "Reunión semanal del equipo de desarrollo", "start_date": "01/06/2025 09:00", "end_date": "01/06/2025 10:30"},
        #         {"titulo": "Cita médica", "descripcion": "Revisión médica anual", "start_date": "01/06/2025 15:00", "end_date": "01/06/2025 16:00"}
        #     ],
        #     5: [
        #         {"titulo": "Cumpleaños de María", "descripcion": "Celebración en el restaurante italiano", "start_date": "05/06/2025 20:00", "end_date": "05/06/2025 23:30"}
        #     ],
        #     17: [
        #         {"titulo": "Dentista", "descripcion": "Limpieza dental rutinaria", "start_date": "17/06/2025 10:00", "end_date": "17/06/2025 11:00"},
        #         {"titulo": "Compras", "descripcion": "Compras semanales en el supermercado", "start_date": "17/06/2025 16:00", "end_date": "17/06/2025 17:30"},
        #         {"titulo": "Gimnasio", "descripcion": "Entrenamiento de piernas", "start_date": "17/06/2025 18:00", "end_date": "17/06/2025 19:30"},
        #         {"titulo": "Cena con amigos", "descripcion": "Cena en el nuevo restaurante asiático", "start_date": "17/06/2025 21:00", "end_date": "17/06/2025 23:00"}
        #     ]
        # }

    # -------------------------------------------------------------------------------------------------------------------------- #
    # DIARY CARD #

    def create_diary_card(self):
        """ Creates the diary card """
        
        # Creating the diary card
        with ui.row().classes('h-fit w-full justify-center md:p-4 p-0'):
            
            # Diary card
            with ui.card().classes('w-full max-w-7xl bg-white rounded-xl shadow-lg overflow-hidden'):
                
                # Diary controls
                self._create_controls()
                
                # Diary sections
                with ui.row().classes('w-full').style('height: 600px'):
                    
                    # Calendar section
                    self._create_calendar_section()
                    
                    # Events section
                    self._create_events_section()
                    
                # Updates the diary component
                self.update_diary()
                self.update_events_panel()

    # -------------------------------------------------------------------------------------------------------------------------- #
    # DIARY METHODS #

    def _create_controls(self):
        """ Creates the diary controllers """
        
        # Calendar controls
        with ui.row().classes('w-full items-center justify-between px-6 py-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-b'):
            
            # Navigation
            with ui.row().classes('items-center gap-3'):
                ui.button(icon='chevron_left', on_click=lambda: self.change_month(-1)) \
                    .props('dense round') \
                    .classes('bg-blue text-blue-600 hover:bg-blue-50 shadow-sm border')
                self.date_label = ui.label().classes('text-2xl font-bold text-gray-800 min-w-[200px] text-center')
                ui.button(icon='chevron_right', on_click=lambda: self.change_month(1)) \
                    .props('dense round') \
                    .classes('bg-blue text-blue-600 hover:bg-blue-50 shadow-sm border')
                    
            # Buttons
            with ui.row().classes('gap-3'):
                ui.button('Hoy', icon='today', on_click=self.go_to_today) \
                    .classes('bg-blue-500 text-white hover:bg-blue-600 px-4 py-2 shadow-sm')
                self.view_button = ui.button('Vista mensual', icon='calendar_view_month', on_click=self.toggle_view_mode) \
                    .props('outline') \
                    .classes('text-blue-600 border-blue-600 hover:bg-blue-50 px-4 py-2')

    def _create_calendar_section(self):
        """ Creates the calendar section """
        
        with ui.column().classes('flex-1 md:p-6 py-6 px-1'):
            self.calendar_container = ui.column().classes('w-full')

    def _create_events_section(self):
        """ Creates the events section """
        
        with ui.column().classes('w-80 bg-gray-50 border-l p-6').style('height: 600px; overflow: hidden;'):
            self.events_container = ui.column().classes('w-full h-full gap-0')


    # -------------------------------------------------------------------------------------------------------------------------- #
    # EVENTS METHODS #

    # def get_events_for_day(self, day):
    #     return self.events_data.get(day, [])
    def get_events_for_day(self, day):
        date_key = self.format_date_title(day, self.calendar_state['month'], self.calendar_state['year'])
        return self.events_data.get(date_key, [])


    def get_all_events_for_month(self):
        month_events = []
        for date_str, events in self.events_data.items():
            try:
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                if date_obj.month == self.calendar_state['month'] and date_obj.year == self.calendar_state['year']:
                    for event in events:
                        event_with_day = event.copy()
                        event_with_day['day'] = date_obj.day
                        event_with_day['date_str'] = date_str  # por si hace falta
                        month_events.append(event_with_day)
            except Exception as e:
                print(f"Error con fecha {date_str}: {e}")
        return sorted(month_events, key=lambda x: (x['day'], x['start_date']))


    def format_date_title(self, day, month, year):
        return f"{day:02d}/{month:02d}/{year}"


    def update_events_panel(self):
        """ Updates the events panel """
        
        # Clearing the events container
        self.events_container.clear()
        
        # Events panel
        with self.events_container:
            
            # Calendar mode
            if self.calendar_state['view_mode'] == 'calendar':
                
                # Creating the events list with the selected day data
                selected_day = self.calendar_state['selected_day']
                events = self.get_events_for_day(selected_day)
                date_title = self.format_date_title(selected_day, self.calendar_state['month'], self.calendar_state['year'])
                
                events_list(
                    events=events,
                    date_title=date_title,
                    on_add=lambda: self.show_event_dialog('create', selected_day),
                    on_edit=lambda event: self.show_event_dialog('edit', selected_day, event),
                    on_delete=lambda event: self.show_event_dialog('delete', selected_day, event)
                )
                
            # Monthly mode    
            else:
                
                # Creating the events list with the selected month data
                month_events = self.get_all_events_for_month()
                month_name = calendar.month_name[self.calendar_state['month']].capitalize()
                year = self.calendar_state['year']
                    
                # Title
                ui.label(f'Eventos de {month_name} {year}').classes('text-lg font-bold text-gray-800 mb-4')
                
                # For each event in the month it creates an event card
                if month_events:
                    current_day = None
                    for event in month_events:
                        if current_day != event['day']:
                            current_day = event['day']
                            if current_day != month_events[0]['day']:
                                ui.separator().classes('my-3')
                            ui.label(f'Día {current_day:02d}').classes('text-sm font-bold text-gray-700 mb-2 mt-3')
                        
                        event_card(
                            event, 
                            on_edit=lambda e: self.select_day_and_edit(event['day'], event),
                            is_monthly=True
                        )
                        
                # No events message
                else:
                    with ui.column().classes('w-full items-center py-8 text-center'):
                        ui.icon('event_busy', size='48px').classes('text-gray-300 mb-2')
                        ui.label('No hay eventos este mes').classes('text-gray-500 font-medium')


    # -------------------------------------------------------------------------------------------------------------------------- #
    # EVENT CARD METHODS #
    
    def select_day_and_edit(self, day, event=None):
        """ Selects the day and edits the event """
        
        # Changes the state and updates the UI
        self.calendar_state['selected_day'] = day
        self.calendar_state['view_mode'] = 'calendar'
        self.update_diary()
        self.update_events_panel()
        self.update_view_button()
        
        # Opens the event dialog
        if event:
            self.show_event_dialog('edit', day, event)


    def show_event_dialog(self, action, day, event=None):
        """ Shows the event dialog """
        
        # If the action is create, the event data is initialized
        if action == 'create':
            event_data = {
                            'day': day,
                            'titulo': '',
                            'descripcion': '',
                            'start_date': f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]} 09:00',
                            'end_date': f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]} 10:00'
                        }
            
        # If the action is edit, the event data is updated
        else:
            event_data = event.copy()
            event_data['day'] = day


        # Hanlding the save event
        # TODO this could be modularized into the dialog function.
        def handle_save(new_event):
            """Manages the save event"""

            day = event_data['day']
            date_key = f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]}'

            # Create event
            if action == 'create':
                if date_key not in self.events_data:
                    self.events_data[date_key] = []
                self.events_data[date_key].append(new_event)
                ui.notify(f'Evento "{new_event["title"]}" creado correctamente', type='positive')

            # Edit event
            else:
                idx = next((i for i, e in enumerate(self.events_data[date_key]) if e['title'] == event['title']), None)
                if idx is not None:
                    self.events_data[date_key][idx] = new_event
                    ui.notify(f'Evento "{new_event["title"]}" actualizado correctamente', type='positive')

            # Updates UI
            self.update_diary()
            self.update_events_panel()


        # Handling the delete event
        def handle_delete(event_to_delete):
            """Manages the delete event"""

            day = event_data['day']
            date_key = f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]}'

            self.events_data[date_key] = [
                e for e in self.events_data[date_key] if e['title'] != event_to_delete['title']
            ]

            if not self.events_data[date_key]:
                del self.events_data[date_key]

            ui.notify(f'Evento "{event_to_delete["title"]}" eliminado correctamente', type='warning')

            # Updates UI
            self.update_diary()
            self.update_events_panel()

        
        # Opens the dialog with the event data and the handlers
        dialog = show_event_dialog(
                                        action=action,
                                        event_data=event_data,
                                        on_save=handle_save,
                                        on_delete=handle_delete if action == 'delete' else None
                                    )
        dialog.open()

    # -------------------------------------------------------------------------------------------------------------------------- #
    # UPDATE METHODS #
    
    def update_diary(self):
        """ Updates the UI of the diary"""
        
        # Clears the calendar container
        self.calendar_container.clear()
        
        # Gets the calendar state
        year = self.calendar_state['year']
        month = self.calendar_state['month']
        selected_day = self.calendar_state['selected_day']
        
        # Updates the UI
        with self.calendar_container:
            if self.calendar_state['view_mode'] == 'calendar':
                calendar_mode(
                                year=year,
                                month=month,
                                selected_day=selected_day,
                                events_data=self.events_data,
                                on_select=self.on_day_select
                            )
            else:
                monthly_mode()
        
        month_name = calendar.month_name[month].capitalize()
        self.date_label.set_text(f"{month_name} {year}")


    def on_day_select(self, day):
        """ Handles the day select event """
        
        # Changes the state
        self.calendar_state['selected_day'] = day
        self.calendar_state['view_mode'] = 'calendar'
        
        # Updates the UI
        self.update_diary()
        self.update_events_panel()
        self.update_view_button()


    def change_month(self, offset):
        
        # Sets the month and year values
        m = self.calendar_state['month'] + offset
        y = self.calendar_state['year']
        
        if m > 12:
            m = 1
            y += 1
        elif m < 1:
            m = 12
            y -= 1
        
        # Changes the state 
        self.calendar_state['month'] = m
        self.calendar_state['year'] = y
        
        # Updates the UI
        self.update_diary()
        self.update_events_panel()


    def go_to_today(self):
        """ Handles the go to today event """
        
        # Changes the state
        today = datetime.today()
        self.calendar_state['year'] = today.year
        self.calendar_state['month'] = today.month
        self.calendar_state['selected_day'] = today.day
        self.calendar_state['view_mode'] = 'calendar'
        
        # Updates the UI
        self.update_diary()
        self.update_events_panel()
        self.update_view_button()


    def toggle_view_mode(self):
        """ Handles the toggle view mode event """
        
        if self.calendar_state['view_mode'] == 'calendar':
            self.calendar_state['view_mode'] = 'monthly'
        else:
            self.calendar_state['view_mode'] = 'calendar'
        
        # Updates the UI
        self.update_diary()
        self.update_events_panel()
        self.update_view_button()


    def update_view_button(self):
        """ Updates the view button """
        
        if self.calendar_state['view_mode'] == 'calendar':
            self.view_button.set_text('Vista mensual')
            self.view_button.props('icon=calendar_view_month')
        else:
            self.view_button.set_text('Vista calendario')
            self.view_button.props('icon=calendar_view_day')