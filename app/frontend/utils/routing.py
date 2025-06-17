# frontend/utils/routing.py

# Import necessary modules
from nicegui import ui
from fastapi.responses import RedirectResponse


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
    def go_diary():
        ui.navigate.to('/diary')
    
    @staticmethod
    def go_events():
        ui.navigate.to('/events')

    @staticmethod
    def go_home2():
        return RedirectResponse(url='/')
        
    @staticmethod    
    def go_login2():
        return RedirectResponse(url='/login')

    @staticmethod
    def go_register2():
        return RedirectResponse(url='/register')

    @staticmethod
    def go_logout2():
        return RedirectResponse(url='/logout')
    
    @staticmethod    
    def go_calendar2():
        return RedirectResponse(url='/calendar')
    
    @staticmethod
    def go_events2():
        return RedirectResponse(url='/events')

    # -------------------------------------------------------------------------------------------- #

    def go_to(self, route: str):
        """ Function to go to a specific route using a function of this class"""
        
        # Routes map -> funtion
        routes_map = {
            '/': RouteHandler.go_home,
            '/login': RouteHandler.go_login,
            '/register': RouteHandler.go_register,
            '/logout': RouteHandler.go_logout,
            '/diary': RouteHandler.go_diary,
            '/events': RouteHandler.go_events,
        }
        
        func = routes_map.get(route)
        
        if func:
            func()
        else:
            ui.notify(f"Route not found: {route}", color='negative')

    def go_to2(self, route: str):
        """ Function to go to a specific route using redirect response"""
        
        # Routes map -> funtion
        routes_map = {
            '/': RouteHandler.go_home2,
            '/login': RouteHandler.go_login2,
            '/register': RouteHandler.go_register2,
            '/logout': RouteHandler.go_logout2,
            '/calendar': RouteHandler.go_calendar2,
            '/events': RouteHandler.go_events2,
        }
        
        func = routes_map.get(route)
        
        if func:
            func()
        else:
            ui.notify(f"Route not found: {route}", color='negative')

# -------------------------------------------------------------------------------------------- #

# Creates a global instance
front_router_handler = RouteHandler()