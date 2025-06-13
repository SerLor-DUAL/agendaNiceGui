# frontend/components/navbar.py

from nicegui import ui
from fastapi.responses import RedirectResponse
from frontend.components.utils.navbar_buttons import navbar_buttons

# Cambia go_to para que retorne RedirectResponse
def go_to(route):
    return RedirectResponse(url=route)

async def navbar():
    with ui.row().classes('items-center justify-between bg-gray-800 p-4 text-white w-full rounded-t'):
        img = ui.image('/static/img/logo.png').classes(
            'w-16 h-auto rounded cursor-pointer hover:opacity-80 transition-opacity duration-300'
        )
        # Al hacer clic, la función go_to retorna RedirectResponse
        img.on('click', lambda _: go_to('/'))

        #with ui.row().classes('space-x-4'):
            #await navbar_buttons()
