# frontend/components/diary/events/events_list.py

# Importing necessary modules
from nicegui import ui
from .event_card import event_card

def events_list(events: list, date_title: str = None, on_add: callable = None, on_edit: callable = None, on_delete: callable = None, is_monthly: bool = False) -> None:
    """Display list of events for the given date or month"""
    
    if date_title:
        _render_header(date_title, on_add)
    
    # Add CSS to hide scrollbars    
    ui.add_head_html("""
                    <style>
                            .hide-scroll .q-scrollarea__container {
                                scrollbar-width: none !important;       /* Firefox */
                                -ms-overflow-style: none !important;    /* IE 10+ */
                                overflow-y: scroll !important;
                            }

                            .hide-scroll .q-scrollarea__container::-webkit-scrollbar {
                                width: 0px !important;
                                height: 0px !important;
                                display: none !important;
                            }
                            
                            .hide-scroll .q-scrollarea__content {
                                padding: 0rem !important;
                            }

                            .hide-scroll .q-scrollarea__thumb {
                                display: none !important;
                                opacity: 0 !important;
                                width: 0 !important;
                                height: 0 !important;
                                pointer-events: none !important;
                                transition: none !important;
                            }

                    </style>
                """)
    
    with ui.scroll_area().classes('h-full w-full pb-4 hide-scroll'):
        _render_events_content(events, on_edit, on_delete, is_monthly)


def _render_header(date_title: str, on_add: callable) -> None:
    """Render events list header with title and add button"""
    
    with ui.row().classes('w-full items-center justify-between mb-4 p-0'):
        
        ui.label(f'Eventos de {date_title}').classes('text-lg font-bold text-gray-800')

        # Add button
        if on_add:
            ui.button(icon='add', color='green', on_click=on_add) \
                .classes('bg-green-500 hover:bg-green-600') \
                .props('dense round size=sm') \
                .tooltip('Agregar evento')


def _render_events_content(events: list, on_edit: callable, on_delete: callable, is_monthly: bool) -> None:
    """Render events content area"""
    if events:
        for event in events:
            event_card(
                            event, 
                            on_edit=lambda e, ev=event: on_edit(ev) if on_edit else None,
                            on_delete=lambda e, ev=event: on_delete(ev) if on_delete else None,
                            is_monthly=is_monthly
                        )
    else:
        _render_empty_state(is_monthly)

def _render_empty_state(is_monthly: bool) -> None:
    """Render empty events state"""
    
    # Message for no events
    message = 'No hay eventos este mes' if is_monthly else 'No hay eventos programados'
    
    with ui.column().classes('w-full items-center py-8 text-center'):
        ui.icon('event_busy', size='48px').classes('text-gray-300 mb-2')
        ui.label(message).classes('text-gray-500 font-medium')