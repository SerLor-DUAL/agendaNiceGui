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
    with ui.grid().classes('w-full md:p-2 py-2 px-0 gap-3 grid grid-cols-7 auto-rows-[75px]'):
        for week in month_days:
            for day in week:
                _render_day_cell(day, month, year, today, selected_day, events_data, on_select)


def _render_weekday_headers() -> None:
    """Renders an adaptative weekday headers for the calendar view."""
    
    # Weekday names
    days_full = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    days_short = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    days_mini = ['L', 'M', 'X', 'J', 'V', 'S', 'D']

    # We add this CSS here because if it's in the global header or external file, it doesn't work properly due to style loading order and dynamic content.
    # Injecting it here ensures the styles apply correctly when the labels are created.
    ui.add_head_html("""
        <style>
            .weekday-label {
                display: block;
            }
            
            .weekday-label::before {
                content: attr(data-mini);
            }
            
            @media (min-width: 425px) and (max-width: 1023px) {
                                            .weekday-label::before {
                                                                        content: attr(data-short);
                                                                    }
                                        }
                                        
            @media (min-width: 1024px) {
                                            .weekday-label::before {
                                                content: attr(data-full);
                                            }
                                        }
        </style>
    """)

    with ui.grid().classes('w-full gap-y-0 px-2 grid-cols-7'):
        for full, short, mini in zip(days_full, days_short, days_mini):
            ui.label("").classes('weekday-label text-center font-medium text-gray-500 text-lg md:text-lg text-md md:text-md py-2 md:py-0') \
            .props(f'data-full="{full}" data-short="{short}" data-mini="{mini}" ')

def _render_day_cell(day: int, month: int, year: int, today: datetime, selected_day: int, events_data: dict, on_select: callable) -> None:
    """Render individual day cell in calendar"""
    
    if day == 0:
        ui.element('div').classes('bg-gray-100 rounded-lg')
        return

    date_key = f'{day:02d}/{month:02d}/{year}'
    
    # Handle case when events_data is None or does not have the key
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