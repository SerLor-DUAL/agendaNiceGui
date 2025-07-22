# frontend/components/diary/diary_card.py

import calendar
import locale
from nicegui import ui
from datetime import datetime
from typing import Dict, List, Optional
from frontend.services.event_services import front_event_service as es
from frontend.components.diary.calendar.calendar_mode import calendar_mode
from frontend.components.diary.events.events_list import events_list
from frontend.components.diary.events.event_dialog import show_event_dialog

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# CSS styles for monthly view
MONTHLY_VIEW_CSS = """
    <style>
        .monthly-container {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 16px;
            padding: 20px;
            min-height: 500px;
        }
        .monthly-header {
            background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
            border-radius: 12px;
            padding: 16px 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        .breadcrumb {
            background: white;
            border-radius: 8px;
            padding: 8px 16px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border-left: 4px solid #3b82f6;
        }
        .stats-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
            border-left: 4px solid #3b82f6;
            transition: all 0.3s ease;
        }
        .stats-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }
        .day-item {
            background: white;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
            border-left: 4px solid #e2e8f0;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .day-item:hover {
            transform: translateX(4px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            border-left-color: #3b82f6;
        }
        .day-event-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
            border-left: 4px solid #3b82f6;
            transition: all 0.3s ease;
        }
        .day-event-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }
        .back-button {
            background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .back-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(107, 114, 128, 0.4);
        }
        .fade-in {
            animation: fadeIn 0.4s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .custom-scroll {
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
        .custom-scroll::-webkit-scrollbar {
            display: none;
            width: 0 !important;
        }
        
        .custom-scroll .q-scrollarea__container {
            scrollbar-width: none !important;       /* Firefox */
            -ms-overflow-style: none !important;    /* IE 10+ */
            overflow-y: scroll !important;
            height: 94% !important;
        }

        .custom-scroll .q-scrollarea__container::-webkit-scrollbar {
            width: 0px !important;
            height: 0px !important;
            display: none !important;
        }

        .custom-scroll .q-scrollarea__content {
            padding: 0rem !important;
            width: 0px !important;
        }

        .custom-scroll .q-scrollarea__content.absolute {
            padding: 0rem !important;
            width: 0px !important;
        }

        .custom-scroll .q-scrollarea__thumb {
            display: none !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            pointer-events: none !important;
            transition: none !important;
        }
    </style>
"""

class DiaryCard:
    def __init__(self, event_data: Dict[str, List[dict]]):
        today = datetime.now()
        self.state = {
            'year': today.year,
            'month': today.month,
            'day': today.day,
            'view': 'daily'  # 'daily' or 'monthly'
        }
        self.events_data = event_data or {}
        self.ui_elements = {
            'date_label': None,
            'calendar_container': None,
            'daily_events_container': None,
            'monthly_container': None,
            'view_button': None
        }
        self.monthly_view_state = {'mode': 'overview', 'selected_day': None}

    # ====================================================================================== #
    # MAIN COMPONENT CONSTRUCTION
    # ====================================================================================== #
    
    def create(self) -> None:
        with ui.row().classes('w-full justify-center p-5'):                
            with ui.card().classes('w-full max-w-7xl bg-white rounded-2xl shadow-2xl p-6'):
                self._create_controls()
                with ui.row().classes('w-full h-[600px] content-start'):
                    self._create_calendar_section()
                    self._create_daily_events_section()
                    self._create_monthly_section()
                self._refresh_ui()

    def _create_controls(self) -> None:
        with ui.row().classes('w-full items-center justify-between px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b rounded-xl'):
            
            # Navigation controls
            with ui.row().classes('items-center gap-3 mr-auto'):
                ui.button(icon='chevron_left', on_click=lambda: self._change_month(-1)) \
                    .classes('text-blue-600 border shadow-sm hover:bg-blue-50')
                
                self.ui_elements['date_label'] = ui.label().classes('text-xl font-bold text-gray-800 min-w-[180px] text-center')
                
                ui.button(icon='chevron_right', on_click=lambda: self._change_month(1)) \
                    .classes('text-blue-600 border shadow-sm hover:bg-blue-50')
            
            # Action buttons
            with ui.row().classes('gap-3'):
                ui.button('Hoy', icon='today', on_click=self._go_to_today) \
                    .classes('bg-blue-500 text-white hover:bg-blue-600 px-4 shadow-sm')
                
                self.ui_elements['view_button'] = ui.button('Vista mensual', icon='calendar_view_month',  on_click=self._toggle_view) \
                    .classes('text-blue-600 border border-blue-600 hover:bg-blue-50 px-4')

    def _create_calendar_section(self) -> None:
        with ui.column().classes('flex-1'):
            self.ui_elements['calendar_container'] = ui.column().classes('w-full p-4')

    def _create_daily_events_section(self) -> None:
        self.ui_elements['daily_events_container'] = ui.column().classes('w-96 bg-gray-50 border-l p-4 h-full')

    def _create_monthly_section(self) -> None:
        self.ui_elements['monthly_container'] = ui.column().classes('w-full hidden')

    # ====================================================================================== #
    # UI REFRESH METHODS
    # ====================================================================================== #
    
    def _refresh_ui(self) -> None:
        self._update_date_label()
        self._update_view_button()
        self._render_calendar()
        
        # Show/hide sections based on current view
        if self.state['view'] == 'daily':
            self.ui_elements['calendar_container'].classes(replace='flex-1 w-full h-full p-4')
            self.ui_elements['daily_events_container'].classes(replace='w-96 bg-gray-50 border-l p-4 h-full')
            self.ui_elements['monthly_container'].classes(replace='fixed hidden top-0 left-0 w-0 h-0')
            self._render_daily_events()
        else:
            self.ui_elements['calendar_container'].classes(replace='fixed hidden top-0 left-0 w-0 h-0')
            self.ui_elements['daily_events_container'].classes(replace='fixed hidden top-0 left-0 w-0 h-0')
            self.ui_elements['monthly_container'].classes(replace='w-full')
            self._render_monthly_view()

    def _update_date_label(self) -> None:
        month_name = calendar.month_name[self.state['month']].capitalize()
        self.ui_elements['date_label'].set_text(f"{month_name} {self.state['year']}")

    def _update_view_button(self) -> None:
        if self.state['view'] == 'daily':
            self.ui_elements['view_button'].set_text('Vista mensual')
            self.ui_elements['view_button'].props('icon=calendar_view_month')
        else:
            self.ui_elements['view_button'].set_text('Vista diaria')
            self.ui_elements['view_button'].props('icon=calendar_view_day')

    def _render_calendar(self) -> None:
        self.ui_elements['calendar_container'].clear()
        with self.ui_elements['calendar_container']:
            calendar_mode(
                            year=self.state['year'],
                            month=self.state['month'],
                            selected_day=self.state['day'],
                            events_data=self.events_data,
                            on_select=self._select_day_in_calendar
                        )

    def _render_daily_events(self) -> None:
        self.ui_elements['daily_events_container'].clear()
        with self.ui_elements['daily_events_container']:
            events = self._get_events_for_day(self.state['day'])
            date_title = self._format_date(self.state['day'])
            
            events_list(
                            events=events,
                            date_title=date_title,
                            on_add=lambda: self._show_event_dialog('create'),
                            on_edit=lambda e: self._show_event_dialog('edit', e),
                            on_delete=lambda e: self._show_event_dialog('delete', e)
                        )

    def _render_monthly_view(self) -> None:
        self.ui_elements['monthly_container'].clear()
        with self.ui_elements['monthly_container']:
            ui.add_head_html(MONTHLY_VIEW_CSS)
            
            if self.monthly_view_state['mode'] == 'overview':
                self._render_monthly_overview()
            else:
                self._render_monthly_day_view()

    # ====================================================================================== #
    # MONTHLY VIEW COMPONENTS
    # ====================================================================================== #
    
    def _render_monthly_overview(self) -> None:
        month_events = self._get_events_for_month()

        with ui.column().classes('w-full monthly-container fade-in'):
            if not month_events:
                self._render_empty_month()
                return
            
            # Month statistics
            self._render_monthly_stats(month_events)

            # Days with events
            self._render_monthly_days_list(month_events)


    def _render_monthly_stats(self, month_events: List[dict]) -> None:
        total_events = len(month_events)
        unique_days = len({e['day'] for e in month_events})
        avg_per_day = total_events / unique_days if unique_days > 0 else 0
        
        # Calculate busiest day
        day_counts = {}
        for event in month_events:
            day = event['day']
            day_counts[day] = day_counts.get(day, 0) + 1
        busiest_day = max(day_counts.items(), key=lambda x: x[1]) if day_counts else (0, 0)
        
        with ui.row().classes('w-full gap-4 mb-6'):
            stats = [
                ('Total eventos', str(total_events), 'text-blue-600'),
                ('Días con eventos', f'{unique_days} días', 'text-green-600'),
                ('Promedio por día', f'{avg_per_day:.1f}', 'text-purple-600'),
                ('Día más ocupado', f'Día {busiest_day[0]} ({busiest_day[1]} eventos)', 'text-red-600')
            ]
            
            for title, value, color_class in stats:
                with ui.column().classes('stats-card flex-1'):
                    ui.label(title).classes('text-sm text-gray-500 font-medium')
                    ui.label(value).classes(f'text-2xl font-bold {color_class}')

    def _render_monthly_days_list(self, month_events: List[dict]) -> None:
        
        # Group events by day
        days_events = {}
        for event in month_events:
            day = event['day']
            days_events.setdefault(day, []).append(event)
        
        ui.label('Días con eventos').classes('text-lg font-bold text-gray-800 p-2')
        
        with ui.scroll_area().classes('h-80 custom-scroll'):
            with ui.column().classes('w-full gap-3 p-3'):
                for day in sorted(days_events.keys()):
                    events = days_events[day]
                    with ui.card().classes('day-item w-full p-3').on('click', lambda d=day: self._select_day_in_monthly_view(d)):
                        with ui.row().classes('w-full items-center justify-between p-4'):
                            
                            # Day info
                            with ui.column().classes('gap-1'):
                                ui.label(f'Día {day:02d}').classes('text-xl font-bold text-gray-800')
                                ui.label(f'{len(events)} eventos').classes('text-sm text-gray-500')
                            
                            # Event preview
                            with ui.row().classes('gap-1 flex-1 mx-4'):
                                for event in events[:8]:
                                    with ui.row().classes('items-center gap-2'):
                                        ui.icon('fiber_manual_record', size='xs').classes('text-blue-500')
                                        ui.label(event['title']).classes('text-sm text-gray-700 truncate')
                                if len(events) > 8:
                                    ui.label(f'+ {len(events) - 2} más').classes('text-xs text-blue-600 font-medium')
                            
                            ui.icon('chevron_right').classes('text-gray-400')


    def _render_monthly_day_view(self) -> None:
        selected_day = self.monthly_view_state['selected_day']
        events = self._get_events_for_day(selected_day)
        date_str = self._format_date(selected_day)
        
        with ui.column().classes('w-full monthly-container gap-1 fade-in max-h-[200px]'):

            # Day header
            with ui.row().classes('w-full monthly-header items-center'):
                with ui.column().classes('flex-1 items-start gap-1'):
                    ui.label(f'{date_str}').classes('text-2xl font-bold text-white')
                    ui.label(f'{len(events)} eventos programados').classes('text-sm text-white/80')
                    
                with ui.row().classes('flex-0 items-end gap-3'):   
                    ui.button(icon='arrow_back', on_click=self._back_to_monthly_overview).classes('back-button')
                    ui.button('Agregar Evento', icon='add', on_click=lambda: self._add_event_to_day(selected_day)) \
                        .classes('bg-white/20 text-white hover:bg-white/30 px-4 py-2')

            # Day events
            if events:
                # with ui.column().classes('w-full gap-4'):
                #     for event in events:
                #         self._render_day_event_card(event)
                with ui.scroll_area().classes('h-80 custom-scroll'):
                    with ui.column().classes('w-full gap-3 p-3'):
                        for event in events:
                            self._render_day_event_card(event)
            else:
                with ui.column().classes('w-full h-60 justify-center items-center'):
                    ui.icon('event_available', size='4xl').classes('text-gray-300 mb-4')
                    ui.label('No hay eventos programados para este día').classes('text-lg text-gray-500')
                    ui.button('Agregar Evento', icon='add', on_click=lambda: self._add_event_to_day(selected_day)) \
                        .classes('bg-blue-600 text-white px-4 py-2 mt-4')

    def _render_day_event_card(self, event: dict) -> None:
        """Render a single event card for the monthly view."""

        with ui.card().classes('day-event-card w-full p-2'):
            with ui.row().classes('items-start justify-between w-full max-w-full p-4'):
                # Columna izquierda: máximo 75% ancho
                with ui.column().classes('flex-grow max-w-[75%] gap-2'):
                    # Título con truncado y tooltip
                    ui.label(event['title']) \
                        .classes('text-lg font-bold text-gray-800 truncate w-full') \
                        .tooltip(event['title'])
                    # Descripción con truncado y tooltip
                    if event.get('description'):
                        ui.label(event['description']) \
                            .classes('text-sm text-gray-600 truncate w-full') \
                            .tooltip(event['description'])
                    # Fecha y hora
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('schedule', size='sm').classes('text-gray-500')
                        start_time = event['start_date'].split(' ')[1] if ' ' in event['start_date'] else event['start_date']
                        end_time = event['end_date'].split(' ')[1] if ' ' in event['end_date'] else event['end_date']
                        ui.label(f'{self._format_iso_to_hour(start_time)} - {self._format_iso_to_hour(end_time)}') \
                            .classes('text-sm text-gray-600')

                # Columna derecha: botones de acción, alineados abajo y pegados a la derecha
                with ui.column().classes('flex-shrink-0 items-end gap-2 min-w-[70px]'):
                    ui.button(icon='edit', on_click=lambda e=event: self._edit_monthly_event(e)) \
                        .classes('text-blue-600 bg-blue-50 hover:bg-blue-100')
                    ui.button(icon='delete', on_click=lambda e=event: self._delete_monthly_event(e)) \
                        .classes('text-red-600 bg-red-50 hover:bg-red-100')

    def _render_empty_month(self) -> None:
        with ui.column().classes('w-full h-96 justify-center items-center fade-in'):
            ui.icon('event_busy').classes('text-gray-300 mb-4').style('font-size: 80px')
            ui.label('No hay eventos este mes').classes('text-xl font-semibold text-gray-600 mb-2')
            ui.label('Los eventos que agregues aparecerán aquí organizados por días') \
                .classes('text-sm text-gray-400 text-center max-w-md')
            ui.button('Agregar Primer Evento', icon='add', 
                     on_click=lambda: self._show_event_dialog('create')) \
                .classes('bg-blue-600 text-white px-6 py-3 mt-4')

    # ====================================================================================== #
    # EVENT DATA METHODS
    # ====================================================================================== #
    
    def _get_events_for_day(self, day: int) -> List[dict]:
        date_key = f'{day:02d}/{self.state["month"]:02d}/{self.state["year"]}'
        return self.events_data.get(date_key, [])

    def _get_events_for_month(self) -> List[dict]:
        month_events = []
        for date_str, events in self.events_data.items():
            try:
                date = datetime.strptime(date_str, '%d/%m/%Y')
                if date.month == self.state['month'] and date.year == self.state['year']:
                    for event in events:
                        event['day'] = date.day
                        month_events.append(event)
            except Exception:
                continue
        return sorted(month_events, key=lambda x: (x['day'], x['start_date']))

    def _format_date(self, day: int) -> str:
        return f"{day:02d}/{self.state['month']:02d}/{self.state['year']}"
    def _format_iso_to_hour(self, datetime_str: str) -> str:
        dt = datetime.fromisoformat(datetime_str)
        return dt.strftime("%H:%M")

    # ====================================================================================== #
    # EVENT HANDLING
    # ====================================================================================== #
    
    def _show_event_dialog(self, action: str, event: Optional[dict] = None) -> None:
        event_data = event.copy() if event else {
                                                    'day': self.state['day'],
                                                    'title': '',
                                                    'description': '',
                                                    'start_date': f'{self._format_date(self.state["day"])} 09:00',
                                                    'end_date': f'{self._format_date(self.state["day"])} 10:00'
                                                }
        if 'day' not in event_data:
            event_data['day'] = self.state['day']

        dialog = show_event_dialog(
            action=action,
            event_data=event_data,
            on_save=lambda e: self._handle_event_save(action, e),
            on_delete=lambda e: self._handle_event_delete(e) if action == 'delete' else None
        )
        dialog.open()

    async def _handle_event_save(self, action: str, new_event: dict) -> None:
        try:
            # Remove backend call here, only notify and refresh
            if action == 'create':
                ui.notify(f'Evento "{new_event["title"]}" creado', type='positive')
            else:
                ui.notify(f'Evento "{new_event["title"]}" actualizado', type='positive')
            
            await self._refresh_events()
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')

    async def _handle_event_delete(self, event: dict) -> None:
        try:
            await es.delete_event(event['id'])
            ui.notify(f'Evento "{event["title"]}" eliminado', type='positive')
            # Elimina el evento localmente para refresco instantáneo
            for events in self.events_data.values():
                events[:] = [e for e in events if e.get('id') != event['id']]
            self._refresh_ui()  # Solo refresca la UI, no recarga del backend (así es más rápido)
        except Exception as e:
            ui.notify(f'Error al eliminar evento: {str(e)}', type='negative')

    async def _refresh_events(self) -> None:
        try:
            loading = ui.linear_progress().classes('w-full absolute top-0')
            ui.update(loading)
            
            self.events_data = await es.get_events()
            self._refresh_ui()
        except Exception as e:
            ui.notify(f'Error actualizando eventos: {str(e)}', type='negative')
        finally:
            if 'loading' in locals():
                loading.delete()

    # ====================================================================================== #
    # NAVIGATION & STATE MANAGEMENT
    # ====================================================================================== #
    
    def _select_day_in_calendar(self, day: int) -> None:
        self.state['day'] = day
        if self.state['view'] == 'daily':
            self._render_daily_events()
        else:
            self.monthly_view_state = {'mode': 'day', 'selected_day': day}
            self._render_monthly_view()
        self._refresh_ui()


    def _change_month(self, delta: int) -> None:
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
        
        today = datetime.now()
        if month == today.month and year == today.year:
            self.state['day'] = today.day
        else:
            self.state['day'] = 1
        
        # Reset monthly view
        self.monthly_view_state = {'mode': 'overview', 'selected_day': None}
        self._refresh_ui()

    def _go_to_today(self) -> None:
        today = datetime.today()
        self.state.update({
            'year': today.year,
            'month': today.month,
            'day': today.day,
        })
        # Reset monthly view
        self.monthly_view_state = {'mode': 'overview', 'selected_day': None}
        self._refresh_ui()

    def _toggle_view(self) -> None:
        self.state['view'] = 'monthly' if self.state['view'] == 'daily' else 'daily'
        # Reset monthly view when switching
        self.monthly_view_state = {'mode': 'overview', 'selected_day': None}
        self._refresh_ui()

    # Monthly view specific methods
    def _select_day_in_monthly_view(self, day: int) -> None:
        self.monthly_view_state = {'mode': 'day', 'selected_day': day}
        self._render_monthly_view()

    def _back_to_monthly_overview(self) -> None:
        self.monthly_view_state = {'mode': 'overview', 'selected_day': None}
        self._render_monthly_view()

    def _add_event_to_day(self, day: int) -> None:
        self.state['day'] = day
        self._show_event_dialog('create')

    def _edit_monthly_event(self, event: dict) -> None:
        day = event.get('day', self.state.get('day', self.monthly_view_state.get('selected_day')))
        self.state['day'] = day
        event_with_day = event.copy()
        event_with_day['day'] = day
        self._show_event_dialog('edit', event_with_day)

    def _delete_monthly_event(self, event: dict) -> None:
        day = event.get('day', self.state.get('day', self.monthly_view_state.get('selected_day')))
        self.state['day'] = day
        event_with_day = event.copy()
        event_with_day['day'] = day
        self._show_event_dialog('delete', event_with_day)