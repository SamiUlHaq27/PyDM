import flet as ft
from loggers import logger
from views import MainView


class App:
    
    def __init__(self, page:ft.Page):
        
        self.page = page
        
        self.main_view = MainView(page)
        
        self.page.on_route_change = self.route_manager
        self.page.go('/')
    
    def route_manager(self, e:ft.RouteChangeEvent):
        if e.route == '/':
            self.page.views.append(self.main_view)
        self.page.update()

if __name__=='__main__':
    ft.app(App)