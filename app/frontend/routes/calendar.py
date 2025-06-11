from datetime import datetime
from nicegui import ui
import httpx
import calendar

from ..components.navbar import navbar
from ..components.headerLinks import header_links


def create_calendar_page():
    """ Create the calendar page """
    header_links()
    navbar()
    create_calendar()

calendar_state = {
    'year': datetime.now().year,
    'month': datetime.now().month,
}

def create_calendar():
     with ui.row().classes('items-center justify-between w-full'):
        ui.button('<', on_click=lambda: change_month(-1)).classes('text-lg')
        label = ui.label().classes('text-2xl font-bold my-4')
        ui.button('>', on_click=lambda: change_month(1)).classes('text-lg')

        calendar_container = ui.column().classes('w-full')

        def change_month(offset: int):
            m = calendar_state['month'] + offset
            if m > 12:
                calendar_state['month'] = 1
                calendar_state['year'] += 1
            elif m < 1:
                calendar_state['month'] = 12
                calendar_state['year'] -= 1
            else:
                calendar_state['month'] = m
            label.text = f"{calendar.month_name[calendar_state['month']]} {calendar_state['year']}"
            update_calendar(calendar_container)

        # Inicialización
        label.text = f"{calendar.month_name[calendar_state['month']]} {calendar_state['year']}"
        update_calendar(calendar_container)

def update_calendar(container):
    container.clear()
    year = calendar_state['year']
    month = calendar_state['month']

    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    days_of_week = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    with container:
        # Grid con 7 columnas
        with ui.grid().style('grid-template-columns: repeat(7, 1fr); gap: 1px; background-color: #ccc').classes('w-full h-full'):
            for day in days_of_week:
                ui.label(day).classes('text-center font-semibold bg-white p-2')

            for week in month_days:
                for day in week:
                    content = str(day) if day != 0 else ""
                    with ui.card().style('min-height: 80px; border: 1px solid #eee; background-color: #fff;'):
                        ui.label(content).classes('text-sm')


