# frontend/components/diary/calendar/calendar_mode.py

# Importing necessary modules
import calendar
from nicegui import ui
from datetime import datetime
from frontend.components.diary.diary_day_card import create_diary_day_card

def calendar_mode(year: int, month: int, selected_day: int, events_data: dict, on_select: callable) -> None:
    """Display calendar view for diary"""
    
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    today = datetime.today()

    # Weekday headers
    _render_weekday_headers()
    
    # Calendar grid
    with ui.grid().classes('w-full p-2 gap-3 grid grid-cols-7 auto-rows-[75px]'):
        for week in month_days:
            for day in week:
                _render_day_cell(day, month, year, today, selected_day, events_data, on_select)

def _render_weekday_headers() -> None:
    """Render weekday header labels"""
    
    days_full = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    days_short = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    with ui.grid().classes('w-full gap-y-0 px-2 grid-cols-7'):
        for day in days_full:
            ui.label(day).classes('hidden md:block text-center font-medium text-gray-500 text-lg')
        for day in days_short:
            ui.label(day).classes('md:hidden text-center font-medium text-gray-500 text-md py-2')

def _render_day_cell(day: int, month: int, year: int, today: datetime, selected_day: int, events_data: dict, on_select: callable) -> None:
    """Render individual day cell in calendar"""
    
    if day == 0:
        ui.element('div').classes('bg-gray-100 rounded-lg')
        return

    date_key = f'{day:02d}/{month:02d}/{year}'
    
    # Manejar caso cuando events_data es None o no tiene la clave
    event_count = 0
    if events_data and date_key in events_data:
        event_count = len(events_data[date_key])
    
    is_today = (day == today.day and month == today.month and year == today.year)
    is_selected = (day == selected_day)
    
    create_diary_day_card(
        day=day,
        event_count=event_count,
        is_today=is_today,
        is_selected=is_selected,
        on_select=lambda d=day: on_select(d)
    )