from nicegui import ui

def create_diary_day_card(day: int, event_count: int, is_today: bool, is_selected: bool, on_select):
    """ Function to create a calendar day card """
    
    if day <= 0:
        return
    
    # Background color
    bg_color = 'bg-white border-2 border-gray-100 shadow-sm hover:shadow-md hover:bg-blue-50 transition-all duration-200'
    if is_today and is_selected:
        bg_color = 'bg-gradient-to-br from-sky-50 to-sky-100 border-2 border-sky-500 shadow-md'
    elif is_today:
        bg_color = 'bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-500 shadow-md'
    elif is_selected:
        bg_color = 'bg-gradient-to-br from-sky-50 to-sky-100 border-2 border-sky-400 shadow-md'
    
    # Card container
    card = ui.card().classes(f'w-full h-full p-1.5 {bg_color} cursor-pointer rounded-lg hover:scale-[1.02] transition-transform duration-150')
    card.on('click', lambda: on_select(day))
    
    with card:
        with ui.column().classes('w-full h-full justify-between'):
            
            # Day number
            with ui.row().classes('w-full justify-end'):
                day_classes = 'text-base font-semibold text-gray-700 select-none'
                if is_today:
                    day_classes = 'text-base font-bold text-blue-700 select-none'
                if is_selected:
                    day_classes = 'text-base font-bold text-sky-700 select-none'
                if is_today and is_selected:
                    day_classes = 'text-base font-bold text-sky-800 select-none'
    
                ui.label(str(day)).classes(day_classes)

            # Events counter
            with ui.row().classes('w-full justify-end items-end'):
                if event_count > 0:
                    badge_classes = 'text-[10px] font-bold bg-blue-500 text-white px-1.5 py-0.5 min-w-[16px] shadow-sm'
                    ui.badge(str(event_count)).classes(badge_classes)