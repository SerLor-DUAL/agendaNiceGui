# frontend/components/diary/diary_card.py

# Import necessary modules
import calendar
import locale
from nicegui import ui
from datetime import datetime
from typing import Dict, List, Optional
from frontend.services.event_services import front_event_service as es
from frontend.components.diary.calendar.calendar_mode import calendar_mode
from frontend.components.diary.events.events_list import events_list
from frontend.components.diary.events.event_dialog import show_event_dialog
from frontend.components.diary.events.event_card import event_card

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# -------------------------------------------------------------------------------------------------- #

# NOTE: This will be the object that contains all the diary related logic and components
class DiaryCard:
    
    # -------------------------------------------------------------------------------------------------- #
    # CONSTRUCTOR #
    
    def __init__(self, event_data: Dict[str, List[dict]]):
        
        # Initialize state variables
        self.state = {
                        'year': datetime.now().year,
                        'month': datetime.now().month,
                        'day': datetime.now().day,
                        'view': 'calendar'              # 'calendar' or 'monthly'
                    }
        
        # Initialize event data
        self.events_data = event_data or {}
        
        # UI elements container
        self.ui_elements = {
                                'date_label': None,
                                'calendar_container': None,
                                'events_container': None,
                                'view_button': None
                            }

    # -------------------------------------------------------------------------------------------------- #
    # DIARY CARD SECTIONS #
    
    def create(self) -> None:
        """Create main diary component"""
        
        with ui.row().classes('w-full justify-center p-4'):                
            
            # Create top controls and sections
            with ui.card().classes('w-full max-w-7xl bg-white rounded-xl shadow-lg'):
                self._create_controls()
            
                # Create calendar and events sections
                with ui.row().classes('w-full h-[600px]'):
                    self._create_calendar_section()
                    self._create_events_section()
                    
                # Initial UI rendering
                self._refresh_ui()


    def _create_controls(self) -> None:
        """Create top control bar"""
        
        with ui.row().classes('w-full items-center justify-between px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b'):
            
            # Navigation
            with ui.row().classes('items-center gap-3'):
                ui.button(icon='chevron_left', on_click=lambda: self._change_month(-1)) \
                    .classes('text-blue-600 border shadow-sm hover:bg-blue-50')
                
                self.ui_elements['date_label'] = ui.label().classes('text-xl font-bold text-gray-800 min-w-[180px] text-center')
                
                ui.button(icon='chevron_right', on_click=lambda: self._change_month(1)) \
                    .classes('text-blue-600 border shadow-sm hover:bg-blue-50')
            
            # Actions
            with ui.row().classes('gap-3'):
                ui.button('Hoy', icon='today', on_click=self._go_to_today) \
                    .classes('bg-blue-500 text-white hover:bg-blue-600 px-4 shadow-sm')
                
                self.ui_elements['view_button'] = ui.button('Vista mensual', icon='calendar_view_month',  on_click=self._toggle_view) \
                    .classes('text-blue-600 border border-blue-600 hover:bg-blue-50 px-4')


    def _create_calendar_section(self) -> None:
        """Create calendar display area"""
        
        # Column inside a column no longer needed, just a single column
        with ui.column().classes('flex-1'):
            self.ui_elements['calendar_container'] = ui.column().classes('w-full p-4')

    def _create_events_section(self) -> None:
        """Create events display area"""
        
        self.ui_elements['events_container'] = ui.column().classes('w-80 bg-gray-50 border-l p-4 h-full')

    # -------------------------------------------------------------------------------------------------- #
    # DATA METHODS #
    
    def _get_events_for_day(self, day: int) -> List[dict]:
        """Get events for specific day"""
        
        date_key = f'{day:02d}/{self.state["month"]:02d}/{self.state["year"]}'
        return self.events_data.get(date_key, [])


    def _get_events_for_month(self) -> List[dict]:
        """Get all events for current month"""
        
        # Initialize empty list for month events
        month_events = []
        
        # Iterate through all events and filter by current month/year
        for date_str, events in self.events_data.items():
            try:
                date = datetime.strptime(date_str, '%d/%m/%Y')
                if date.month == self.state['month'] and date.year == self.state['year']:
                    for event in events:
                        event['day'] = date.day
                        month_events.append(event)
            except Exception:
                continue
        
        # Sort events by day and start date
        return sorted(month_events, key=lambda x: (x['day'], x['start_date']))


    def _format_date(self, day: int) -> str:
        """Format date as DD/MM/YYYY"""
        
        return f"{day:02d}/{self.state['month']:02d}/{self.state['year']}"

    # -------------------------------------------------------------------------------------------------- #
    # UI RENDERING #
    
    def _refresh_ui(self) -> None:
        """Refresh all UI components"""
        
        self._update_date_label()
        self._render_calendar()
        self._render_events()
        self._update_view_button()


    def _update_date_label(self) -> None:
        """Update month/year display label"""
        month_name = calendar.month_name[self.state['month']].capitalize()
        self.ui_elements['date_label'].set_text(f"{month_name} {self.state['year']}")


    @ui.refreshable
    def _render_calendar(self) -> None:
        """Render calendar view"""
        
        self.ui_elements['calendar_container'].clear()
        with self.ui_elements['calendar_container']:
            if self.state['view'] == 'calendar':
                self.ui_elements['calendar_container'].props('class="nicegui-column w-full p-4"')
                calendar_mode(
                                year=self.state['year'],
                                month=self.state['month'],
                                selected_day=self.state['day'],
                                events_data=self.events_data,
                                on_select=self._select_day
                            )
            else:
                self.ui_elements['calendar_container'].props('class="nicegui-column w-full p-0 hidden"')

    @ui.refreshable
    def _render_events(self) -> None:
        """Render events panel"""
        
        self.ui_elements['events_container'].clear()
        with self.ui_elements['events_container']:
            if self.state['view'] == 'calendar':
                self.ui_elements['events_container'].props('class="nicegui-column w-80 bg-gray-50 border-l p-4 h-full overflow-hidden"')
                self._render_daily_events()
            else:
                self.ui_elements['events_container'].props('class="nicegui-column w-full bg-gray-50 border-l p-4 h-[90%] overflow-hidden"')
                self._render_monthly_events()


    def _render_daily_events(self) -> None:
        """Render daily events view"""
        
        events = self._get_events_for_day(self.state['day'])
        date_title = self._format_date(self.state['day'])
        
        events_list(
                        events=events,
                        date_title=date_title,
                        on_add=lambda: self._show_event_dialog('create'),
                        on_edit=lambda e: self._show_event_dialog('edit', e),
                        on_delete=lambda e: self._show_event_dialog('delete', e)
                    )


    def _render_monthly_events(self) -> None:
        """Render monthly events view"""
        
        month_events = self._get_events_for_month()
        month_name = calendar.month_name[self.state['month']].capitalize()
        
        ui.label(f'Eventos de {month_name} {self.state["year"]}').classes('text-lg font-bold text-gray-800 mb-4')
        # with ui.scroll_area().classes('h-full w-[50%] pb-4 hide-scrollbar'):    
        if not month_events:
            self._render_empty_month()
            return
        with ui.row().classes('w-full h-full overflow-y-hidden overflow-x-auto flex-nowrap gap-4'):
            # with ui.scroll_area().classes('h-full w-full pb-4 horizontal-scrollbar'):
            #     with ui.row().classes('gap-4 w-full h-max overflow-x-scroll flex-nowrap'):
            current_day = None
            for event in month_events:
                if current_day != event['day']:
                    current_day = event['day']
                    with ui.column().classes('w-1/4 h-full flex-shrink-0 items-center overflow-y-auto bg-gray-100 p-3'): 
                        ui.label(f'Día {current_day:02d}').classes('text-sm font-bold text-gray-700 mb-2 mt-3')
                        for event in month_events:
                            if event['day'] == current_day:
                                # Render event card for the specific day
                                event_card(
                                            event,
                                            on_edit=lambda e: self._select_day_and_edit(e),
                                            is_monthly=True
                                        )


    def _render_empty_month(self) -> None:
        """Render empty monthly events state"""
        
        with ui.column().classes('w-full items-center py-8 text-center'):
            ui.icon('event_busy', size='48px').classes('text-gray-300 mb-2')
            ui.label('No hay eventos este mes').classes('text-gray-500 font-medium')


    def _update_view_button(self) -> None:
        """Update view toggle button text/icon"""
        
        
        if self.state['view'] == 'calendar':
            self.ui_elements['view_button'].set_text('Vista mensual')
            self.ui_elements['view_button'].props('icon=calendar_view_month')
        else:
            self.ui_elements['view_button'].set_text('Vista calendario')
            self.ui_elements['view_button'].props('icon=calendar_view_day')

    # -------------------------------------------------------------------------------------------------- #
    # CALENDAR HANDLING FUNCTIONS #
    
    def _select_day(self, day: int) -> None:
        """Handle day selection"""
        
        self.state['day'] = day
        self.state['view'] = 'calendar'
        self._refresh_ui()


    def _change_month(self, delta: int) -> None:
        """Change current month view"""
        
        month = self.state['month'] + delta
        year = self.state['year']
        
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
        
        self.state['month'] = month
        self.state['year'] = year
        self._refresh_ui()


    def _go_to_today(self) -> None:
        """Navigate to current date"""
        today = datetime.today()
        self.state.update({
            'year': today.year,
            'month': today.month,
            'day': today.day,
            'view': 'calendar'
        })
        self._refresh_ui()


    def _toggle_view(self) -> None:
        """Toggle between calendar and monthly views"""
        self.state['view'] = 'monthly' if self.state['view'] == 'calendar' else 'calendar'
        self._refresh_ui()

    # TODO Sergio doesnt like names :(
    def _select_day_and_edit(self, event: dict) -> None:
        """Select day and open event editor"""
        self.state['day'] = event['day']
        self.state['view'] = 'calendar'
        self._refresh_ui()
        self._show_event_dialog('edit', event)

    # -------------------------------------------------------------------------------------------------- #
    # EVENT DIALOG HANDLING FUNCTIONS #

    async def _show_event_dialog(self, action: str, event: Optional[dict] = None) -> None:
        """Show event CRUD dialog"""
        
        if action == 'create':
            event_data = {
                            'day': self.state['day'],
                            'title': '',
                            'description': '',
                            'start_date': f'{self._format_date(self.state["day"])} 09:00',
                            'end_date': f'{self._format_date(self.state["day"])} 10:00'
                        }
        else:
            event_data = event.copy()
            event_data['day'] = self.state['day']

        dialog = show_event_dialog(
                                    action=action,
                                    event_data=event_data,
                                    on_save=lambda e: self._handle_event_save(action, e),
                                    on_delete=lambda e: self._handle_event_delete(e) if action == 'delete' else None
                                )
        dialog.open()


    async def _handle_event_save(self, action: str, new_event: dict) -> None:
        """Handle event save from dialog"""
        
        try:
            date_key = self._format_date(self.state['day'])
            
            if action == 'create':
                self.events_data.setdefault(date_key, []).append(new_event)
                ui.notify(f'Evento "{new_event["title"]}" creado', type='positive')
            else:
                events = self.events_data[date_key]
                index = next(i for i, e in enumerate(events) if e['id'] == new_event['id'])
                events[index] = new_event
                ui.notify(f'Evento "{new_event["title"]}" actualizado', type='positive')
            
            await self._refresh_events()
            
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')


    async def _handle_event_delete(self, event: dict) -> None:
        """Handle event deletion from dialog"""
        
        try:
                if 'id' not in event:
                    raise ValueError("ID de evento no encontrado")
                
                # Obtener la clave de fecha
                date_key = self._format_date(self.state['day'])
                
                # Verificar si la fecha existe en los eventos
                if date_key not in self.events_data:
                    ui.notify('El evento ya ha sido eliminado', type='warning')
                    return
                    
                # Filtrar el evento a eliminar
                initial_events = self.events_data[date_key]
                updated_events = [e for e in initial_events if e['id'] != event['id']]
                
                # Actualizar o eliminar la fecha según si quedan eventos
                if updated_events:
                    self.events_data[date_key] = updated_events
                else:
                    # Eliminar la fecha completamente si no quedan eventos
                    del self.events_data[date_key]
                
                ui.notify(f'Evento "{event["title"]}" eliminado exitosamente!', type='positive')
                
                # Actualizar solo los componentes afectados
                self._render_events.refresh()
                self._render_calendar.refresh()
                
        except Exception as e:
            ui.notify(f'Error al eliminar evento: {str(e)}', type='negative')
            await self._refresh_events()


    async def _refresh_events(self) -> None:
        """Refresh events from backend"""
        import asyncio
        
        try:
            # Usar un indicador de carga más confiable
            loading = ui.linear_progress().classes('w-full absolute top-0')
            ui.update(loading)
            
            # Obtener eventos con manejo de timeout
            try:
                self.events_data = await asyncio.wait_for(es.get_events(), timeout=8.0)
            except asyncio.TimeoutError:
                ui.notify('El servidor está tardando en responder', type='warning')
                # Intentar nuevamente con un timeout más corto
                self.events_data = await asyncio.wait_for(es.get_events(), timeout=4.0)
            
            # Actualizar UI
            self._render_events.refresh()
            self._render_calendar.refresh()
            
        except asyncio.TimeoutError:
            ui.notify('No se pudo obtener la lista de eventos', type='negative')
        except Exception as e:
            ui.notify(f'Error actualizando eventos: {str(e)}', type='negative')
        finally:
            if loading:
                loading.delete()