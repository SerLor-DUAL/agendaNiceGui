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
from frontend.services.event_services import front_event_service as es                  # Importing the event service

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
        
        # Data
        self.events_data = event_data if event_data is not None else {}


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
                    
                # Updates the diary components
                self.render_calendar()
                self.render_events()

    # -------------------------------------------------------------------------------------------------------------------------- #
    # DIARY CARD ADDONS #

    def _create_controls(self):
        """ Creates the diary controllers """
        
        # Calendar controls
        with ui.row().classes('w-full items-center justify-between px-6 py-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-b'):
            
            # Navigation
            with ui.row().classes('items-center gap-3'):
                
                # Previous month button
                ui.button(icon='chevron_left', on_click=lambda: self.change_month(-1)).props('dense round') \
                    .classes('bg-blue text-blue-600 hover:bg-blue-50 shadow-sm border')
                
                # Date label    
                self.date_label = ui.label().classes('text-2xl font-bold text-gray-800 min-w-[200px] text-center')
                
                #  Next month button
                ui.button(icon='chevron_right', on_click=lambda: self.change_month(1)).props('dense round') \
                    .classes('bg-blue text-blue-600 hover:bg-blue-50 shadow-sm border')
                    
            # Action buttons
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
        
        self.events_container = ui.column().classes('w-80 bg-gray-50 border-l p-6 h-full gap-0').style('height: 600px; overflow: hidden;')


    # -------------------------------------------------------------------------------------------------------------------------- #
    # EVENTS GENERAL METHODS #

    def get_events_for_day(self, day):
        """ Returns the events for a specific day """
        
        # It gets the events for the specified day formatting the date key to a displayable format
        date_key = self.format_date_title(day, self.calendar_state['month'], self.calendar_state['year'])
        
        # Returns the events for the specified date key, or an empty list if there are no events
        return self.events_data.get(date_key, [])


    def get_all_events_for_month(self):
        """ Returns all events for the current month """
        
        month_events = []
        
        # Iterates through the events data and filters the events for the current month
        for date_str, events in self.events_data.items():
            
            # Parses the date string to a datetime object and checks if the month and year match the current calendar state
            try:
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                if date_obj.month == self.calendar_state['month'] and date_obj.year == self.calendar_state['year']:
                    
                    # If it matches, it adds the events to the month_events list with the day and date_str
                    for event in events:
                        event_with_day = event.copy()
                        event_with_day['day'] = date_obj.day    # Adding the day of the month
                        event_with_day['date_str'] = date_str   # Adding the original date string for reference
                        month_events.append(event_with_day)     # Adding the event to the month list
            
            # If there's an error parsing the date, it prints the error and continues
            except Exception as e:
                print(f"Error con fecha {date_str}: {e}")
                
        # Sorts the month events by day and start date
        return sorted(month_events, key=lambda x: (x['day'], x['start_date']))


    def format_date_title(self, day, month, year):
        """ Formats the date title for display """
    
        return f"{day:02d}/{month:02d}/{year}"

    @ui.refreshable
    def render_events(self):
        """ Renders and refreshes the events panel """
        
        # Clearing the events container
        self.events_container.clear()
        
        # Events panel
        with self.events_container:
            
            # Calendar mode
            if self.calendar_state['view_mode'] == 'calendar':
                
                # Change the width according to the mode
                self.events_container.props('class="w-80 bg-gray-50 border-l p-6 h-full gap-0"')
                
                # Creates the events list with the selected day data
                selected_day = self.calendar_state['selected_day']
                
                # Retrieves the events for the selected day
                events = self.get_events_for_day(selected_day)
                
                # Formats the date title for display of the selected day
                date_title = self.format_date_title(selected_day, self.calendar_state['month'], self.calendar_state['year'])
                
                # Creates the list of events for the selected day
                events_list(
                            events=events,                                                                          # Events for the selected day
                            date_title=date_title,                                                                  # Date of the selected day                                                     
                            on_add=lambda: self.show_event_dialog('create', selected_day),                          # Function to add a new event    
                            on_edit=lambda event: self.show_event_dialog('edit', selected_day, event),              # Function to edit an existing event
                            on_delete=lambda event: self.show_event_dialog('delete', selected_day, event)           # Function to delete an existing event
                        )
                
            # Monthly mode    
            else:
                # Change the width according to the mode
                self.events_container.props('class="w-full bg-gray-50 border-l p-6 h-full gap-0"')

                # Creates the events list with the selected month data
                month_events = self.get_all_events_for_month()
                
                # Formats the month name and year for the title
                month_name = calendar.month_name[self.calendar_state['month']].capitalize()
                
                # If the year is not set, it uses the current year
                year = self.calendar_state['year']
                    
                # Title for the events list of the month
                ui.label(f'Eventos de {month_name} {year}').classes('text-lg font-bold text-gray-800 mb-4')
                
                # For each event in the month it creates an event card
                if month_events:

                    current_day = None
                    
                    # Iterates through the month events and creates an event card for each one separated by day
                    for event in month_events:
                        if current_day != event['day']:
                            current_day = event['day']
                            
                            # If the day has changed, it adds a separator and a label for the day
                            if current_day != month_events[0]['day']:
                                ui.separator().classes('my-3')
                            ui.label(f'Día {current_day:02d}').classes('text-sm font-bold text-gray-700 mb-2 mt-3')
                        
                        # Creates the event card for the event
                        event_card(
                                        event,                                                                  # The event data
                                        on_edit=lambda e: self.select_day_and_edit(event['day'], event),        # Function to edit the event
                                        is_monthly=True                                                         # Indicates that it is a monthly event card     
                                    )
                        
                # No events message
                else:
                    with ui.column().classes('w-full items-center py-8 text-center'):
                        ui.icon('event_busy', size='48px').classes('text-gray-300 mb-2')
                        ui.label('No hay eventos este mes').classes('text-gray-500 font-medium')


    # -------------------------------------------------------------------------------------------------------------------------- #
    # EVENT CARD SPECIFIC METHODS #
    
    def select_day_and_edit(self, day, event=None):
        """ Selects the day and edits the event from the event card """
        
        # Changes the state and updates the UI
        self.calendar_state['selected_day'] = day
        self.calendar_state['view_mode'] = 'calendar'
        
        # Updates the diary and events panel
        self.render_calendar()
        self.render_events()
        self.update_view_button()
        
        # Opens the event dialog
        if event:
            self.show_event_dialog('edit', day, event)


    async def show_event_dialog(self, action, day, event=None):
        """ Show an event dialog to create, edit or delete an event in the current list of events for the selected day """
        
        # If the action is create, the event data is initialized
        if action == 'create':
            event_data = {
                            'day': day,
                            'title': '',
                            'description': '',
                            'start_date': f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]} 09:00',
                            'end_date': f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]} 10:00'
                        }
            
        # If the action is edit or delete, the event data is updated copying the existing event data
        else:
            event_data = event.copy()
            event_data['day'] = day

        # Variable to store dialog reference
        dialog = None
        
        # Hanlding the save event
        async def handle_save(new_event):
            """Manages the save event from the dialog"""

            try:
                # Extracts the actual day and formats the date key
                day = event_data['day']
                date_key = f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]}'

                # Creates a new event
                if action == 'create':
                    
                    if new_event:
                        # Add the event with the ID created by the backend
                        if date_key not in self.events_data:
                            self.events_data[date_key] = []
                        
                        # Use the complete event returned by the backend (which includes the ID)
                        self.events_data[date_key].append(new_event)
                        
                        # Notify the user that the event was created successfully
                        ui.notify(f'Evento "{new_event["title"]}" creado correctamente', type='positive')
                        
                    # If the event creation fails, notify the user
                    else:
                        print('Error al crear el evento', type='negative')
                        return

                # Edit event
                else:

                    if new_event:
                        # Updates the local events data with the updated event
                        if date_key in self.events_data:
                            idx = next((i for i, e in enumerate(self.events_data[date_key]) if e['id'] == event['id']), None)
                            
                            if idx is not None:
                                self.events_data[date_key][idx] = new_event
                                
                        # Notify the user that the event was updated successfully
                        ui.notify(f'Evento "{new_event["title"]}" actualizado correctamente', type='positive')
                            
                    # If the event update fails, notify the user
                    else:
                        print('Error al actualizar el evento', type='negative')
                        return

                # Update UI immediately after successful operation
                await self.refresh_events_from_backend()
                
                # Close the dialog
                if dialog:
                    dialog.close()
                    
            except Exception as e:
                print(f"Error in handle_save: {e}")
                ui.notify('Error inesperado al guardar el evento', type='negative')


        # Handling the delete event
        async def handle_delete(event_to_delete):
            """Manages the delete event"""

            try:

                # Checks if the event to delete has ID
                if 'id' not in event_to_delete:
                    print('El evento no tiene un identificador único para eliminarlo', type='negative')
                    return
                
                if event_to_delete:

                    day = event_data['day']
                    date_key = f'{day:02d}/{self.calendar_state["month"]:02d}/{self.calendar_state["year"]}'

                    # Deletes the event from the local events data
                    if date_key in self.events_data:
                        self.events_data[date_key] = [e for e in self.events_data[date_key] if e['id'] != event_to_delete['id']]
                        
                        # If there are no more events for that date, it removes the date key from the events data
                        if not self.events_data[date_key]:
                            del self.events_data[date_key]
                    
                    # Notify the user that the event was deleted successfully
                    ui.notify(f'Evento "{event_to_delete["title"]}" eliminado correctamente', type='warning')
                    
                    # Update UI immediately after successful operation
                    await self.refresh_events_from_backend()
                    
                    # Close the dialog
                    if dialog:
                        dialog.close()
                    
                # If the event deletion fails, notify the user
                else:
                    print('Error al eliminar el evento', type='negative')
                    return
                    
            except Exception as e:
                print(f"Error in handle_delete: {e}")
                ui.notify('Error inesperado al eliminar el evento', type='negative')
            
        # Opens the dialog with the event data and the handlers
        dialog = show_event_dialog(
                                        action=action,
                                        event_data=event_data,
                                        on_save=handle_save,
                                        on_delete=handle_delete if action == 'delete' else None
                                    )
        dialog.open()

        
    def convert_date_to_backend_format(self, date_str):
        """Converts a date string from the frontend format to the backend format"""
        try:
            dt = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
            return dt.strftime('%Y-%m-%dT%H:%M:%S')
        except Exception as e:
            print(f"Error convirtiendo fecha {date_str}: {e}")
            return date_str

    async def refresh_events_from_backend(self):
        """Refreshes the events from the backend"""
        try:
            # Obtain the updated events from the event service that calls the backend
            updated_events = await es.get_events()
            
            # Update the events data
            if updated_events:
                self.events_data = updated_events

            # Update the UI
            ui.timer(0.0001, lambda: self._refresh_ui(), once=True)

        except Exception as e:
            print(f"Error refreshing events: {e}")
            ui.notify('Error al actualizar eventos', type='negative')

    def _refresh_ui(self):
        """ Refreshes the UI components """
        
        # Refreshes the calendar and events
        self.render_calendar()
        self.render_events()
        
        # Updates the view button
        self.update_view_button()
    
    # -------------------------------------------------------------------------------------------------------------------------- #
    # UPDATE METHODS #
    
    @ui.refreshable
    def render_calendar(self):
        """ Renders and refreshes the UI of the calendar"""
        
        # Clears the calendar container
        self.calendar_container.clear()
        
        # Gets the calendar state
        year = self.calendar_state['year']
        month = self.calendar_state['month']
        selected_day = self.calendar_state['selected_day']
        
        # Updates the UI
        with self.calendar_container:
            if self.calendar_state['view_mode'] == 'calendar':
                self.calendar_container.props('class="w-full"')
                calendar_mode(
                                year=year,
                                month=month,
                                selected_day=selected_day,
                                events_data=self.events_data,
                                on_select=self.on_day_select
                            )
            else:
                self.calendar_container.props('class="hidden p-0"')
                monthly_mode()
        
        month_name = calendar.month_name[month].capitalize()
        self.date_label.set_text(f"{month_name} {year}")


    def on_day_select(self, day):
        """ Handles the day select event """
        
        # Changes the state
        self.calendar_state['selected_day'] = day
        self.calendar_state['view_mode'] = 'calendar'
        
        # Updates the UI
        self.render_calendar()
        self.render_events()
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
        self.render_calendar()
        self.render_events()


    def go_to_today(self):
        """ Handles the go to today event """
        
        # Changes the state
        today = datetime.today()
        self.calendar_state['year'] = today.year
        self.calendar_state['month'] = today.month
        self.calendar_state['selected_day'] = today.day
        self.calendar_state['view_mode'] = 'calendar'
        
        # Updates the UI
        self.render_calendar()
        self.render_events()
        self.update_view_button()


    def toggle_view_mode(self):
        """ Handles the toggle view mode event """
        
        if self.calendar_state['view_mode'] == 'calendar':
            self.calendar_state['view_mode'] = 'monthly'
        else:
            self.calendar_state['view_mode'] = 'calendar'
        
        # Updates the UI
        self.render_calendar()
        self.render_events()
        self.update_view_button()


    def update_view_button(self):
        """ Updates the view button """
        
        if self.calendar_state['view_mode'] == 'calendar':
            self.view_button.set_text('Vista mensual')
            self.view_button.props('icon=calendar_view_month')
        else:
            self.view_button.set_text('Vista calendario')
            self.view_button.props('icon=calendar_view_day')