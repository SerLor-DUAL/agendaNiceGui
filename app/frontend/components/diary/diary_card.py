# frontend/components/diary/diary_card.py

# Import necessary modules
import calendar                                                                         # Import the calendar module 
from nicegui import ui                                                                  # Import the ui module
from datetime import datetime                                                           # Import the datetime module
from frontend.components.diary.diary_day_card import create_diary_day_card              # Import the create_diary_day_card function

# Global calendar state
calendar_state = {'year': datetime.now().year, 'month': datetime.now().month, }

# NOTE: Function to create a calendar card
def diary_card():

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # METHODS #

    def add_day_card(day: int):
        """ Adds a day card to the calendar """
        create_diary_day_card(day)


    def update_diary(container, date_label):
        """ Updates the calendar """
        
        # Clear the container
        container.clear()

        # Get the current year and month
        year = calendar_state['year']
        month = calendar_state['month']

        # Create the calendar object
        cal = calendar.Calendar(firstweekday=0)
        
        # Get the days of the month
        month_days = cal.monthdayscalendar(year, month)
        
        # Get the days of the week
        days_of_week = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

        # Renders the calendar
        with container:
            
            # Renders the days of the week
            with ui.grid().classes('w-full p-2 rounded gap-2').style('grid-template-columns: repeat(7, 1fr); background-color: #ccc'):
                
                # Renders the day labels
                for day in days_of_week:
                    ui.label(day).classes('text-center font-semibold bg-white p-2')

                # Renders the day cards
                for week in month_days:
                    for day in week:
                        add_day_card(day)

        # Updates the label with the month and year
        date_label.text = f"{calendar.month_name[month]} {year}"


    def change_month(offset: int, container, date_label):
        """ Changes the month and updates the calendar """
        
        # Get the current month and year
        m = calendar_state['month'] + offset
        y = calendar_state['year']

        # Check if the month is out of range and adjust
        if m > 12:
            m = 1
            y += 1
        elif m < 1:
            m = 12
            y -= 1

        # Updates the month and year
        calendar_state['month'] = m
        calendar_state['year'] = y

        # Updates the calendar refreshing the container
        update_diary(container, date_label)

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # UI #

    # Calendar card
    with ui.row().classes('w-full p-8 h-100 bg-gray-100 rounded shadow'):
        
        # Calendar header
        with ui.row().classes('items-center justify-between w-full'):
            
            # Calendar buttons and date label
            btn_prev = ui.button('<').classes('text-lg')
            date_label = ui.label().classes('text-2xl font-bold my-4')
            btn_next = ui.button('>').classes('text-lg')

        # Calendar container
        calendar_container = ui.row().classes('w-full')

        # Button events
        btn_prev.on('click', lambda e: change_month(-1, calendar_container, date_label))
        btn_next.on('click', lambda e: change_month(1, calendar_container, date_label))

        # Initial render
        update_diary(calendar_container, date_label)
