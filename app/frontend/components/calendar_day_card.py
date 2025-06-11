# components/calendar_day_card.py

from nicegui import ui

def CalendarDayCard(day: int, year: int, month: int):
    """Un componente de celda de día en el calendario"""
    with ui.card().style('min-height: 80px; border: 1px solid #eee; background-color: #fff;'):
        if day > 0:
            ui.label(str(day)).classes('text-sm font-medium')
            # NOTE here you can add more details about the day, like events or tasks
            # For example a icon or label for events
        else:
            ui.label("").classes('text-sm')
