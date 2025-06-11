from nicegui import ui
import httpx

from ..components.navbar import navbar
from ..components.headerLinks import header_links

async def create_calendar_page():
    # Check if the user is authenticated

    header_links()
    navbar()
