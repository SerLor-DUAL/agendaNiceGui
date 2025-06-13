# frontend/utils/routing.py

# Import necessary modules
from nicegui import ui

# NOTE: Class to handle routing in the frontend elements
        # This is due to the fact that the components have a problem with the lambda redirecting
        # TODO: Check why and make some explanation here to clarify
class RouteHandler:

    @staticmethod
    def go_home():
        ui.navigate.to('/')
        
    @staticmethod    
    def go_login():
        ui.navigate.to('/login')

    @staticmethod
    def go_register():
        ui.navigate.to('/register')

    @staticmethod
    def go_logout():
        ui.navigate.to('/logout')
    
    @staticmethod    
    def go_calendar():
        ui.navigate.to('/calendar')
    
    @staticmethod
    def go_events():
        ui.navigate.to('/events')

    # -------------------------------------------------------------------------------------------- #

    def go_to(self, route: str):
        """ Function to go to a specific route using a function of this class"""
        
        # Routes map -> funtion
        routes_map = {
            '/': RouteHandler.go_home,
            '/login': RouteHandler.go_login,
            '/register': RouteHandler.go_register,
            '/logout': RouteHandler.go_logout,
            '/calendar': RouteHandler.go_calendar,
            '/events': RouteHandler.go_events,
        }
        
        func = routes_map.get(route)
        
        if func:
            func()
        else:
            ui.notify(f"Route not found: {route}", color='negative')


# -------------------------------------------------------------------------------------------- #

# Creates a global instance
front_router_handler = RouteHandler()