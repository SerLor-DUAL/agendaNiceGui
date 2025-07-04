# frontend/components/diary/calendar/calendar_mode.py

# Import necessary modules
import calendar                                                                     # Importing for calendar operations                  
from nicegui import ui                                                              # Importing for GUI operations
from datetime import datetime                                                       # Importing for date and time operations
from frontend.components.diary.diary_day_card import create_diary_day_card          # Importing for creating diary day cards

def calendar_mode(year, month, selected_day, events_data, on_select):
    """ Calendar mode for the diary """
    
    # Create a calendar object
    cal = calendar.Calendar(firstweekday=0)
    
    # Get the days of the month
    month_days = cal.monthdayscalendar(year, month)
    
    # Assign the weekdays naming
    days_of_week = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    # Responsive Weekdays naming
    days_of_week_responsive = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    # Get the current date
    today = datetime.today()
    
    # Display the calendar weekdays in a grid
    with ui.grid().classes('w-full gap-y-0 px-2').style('grid-template-columns:repeat(7, minmax(0, 1fr));'):
        for day in days_of_week:
            ui.label(day).classes('text-center font-medium text-gray-500 text-lg opacity-0 lg:opacity-100 lg:h-auto h-0 pb-0 lg:pb-3 pt-0 lg:pt-1')
        for day in days_of_week_responsive:
            ui.label(day).classes('text-center font-medium text-gray-500 text-md h-auto lg:hidden lg:h-0 pt-2 lg:pt-0 pb-3 lg:pb-0')

    # Display the calendar days in a grid
    with ui.grid().classes('w-full p-2 gap-3').style('grid-template-columns: repeat(7, minmax(0, 1fr)); grid-auto-rows: 75px;'):
        for i in range(6):
            week = month_days[i] if i < len(month_days) else [0]*7
            for day in week:

                # Create a placeholder for empty days
                if day == 0:
                    ui.element('div').classes('bg-gray-100 shadow-lg rounded-lg')

                # Create a day card
                else:
                    date_key = f'{day:02d}/{month:02d}/{year}'
                    event_count = len(events_data.get(date_key, []) if events_data is not None else [])
                    is_today = (day == today.day and month == today.month and year == today.year)
                    is_selected = (day == selected_day)
                    create_diary_day_card(day, event_count, is_today, is_selected, lambda d=day: on_select(d))