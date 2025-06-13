from nicegui import ui                                                    # Import the ui module
from frontend.services.auth_services import front_auth_service as auth    # Import the AuthService instance


async def create_logout_page():
    await auth.logout()
    ui.navigate.to("/")