import flet as ft


class TitleBar(ft.WindowDragArea):
    
    def __init__(self, page:ft.Page):
        self.fullscreen_btn = ft.IconButton(ft.icons.FULLSCREEN, on_click=self.fullscreen_btn_clicked)
        self.exit_fullscreen_btn = ft.IconButton(ft.icons.FULLSCREEN_EXIT, on_click=self.exit_fullscreen_btn_clicked)
        self.content = ft.Row([
            ft.IconButton(ft.icons.MINIMIZE, on_click=self.minimized_btn_clicked),
            self.fullscreen_btn,
            self.exit_fullscreen_btn,
            ft.IconButton(ft.icons.CLOSE, on_click=self.close_btn_clicked)
        ], alignment=ft.MainAxisAlignment.END)
        super(TitleBar, self).__init__(self.content)
        
        self.page = page
    
    def before_update(self):
        if self.page.window.maximized:
            self.fullscreen_btn.visible = False
            self.exit_fullscreen_btn.visible = True
        else:
            self.fullscreen_btn.visible = True
            self.exit_fullscreen_btn.visible = False
    
    def close_btn_clicked(self, e):
        self.page.window.close()
    
    def fullscreen_btn_clicked(self, e):
        self.page.window.maximized = True
        self.page.update()
    
    def exit_fullscreen_btn_clicked(self, e):
        self.page.window.maximized = False
        self.page.update()
    
    def minimized_btn_clicked(self, e):
        self.page.window.minimized = True
        self.page.update()

class ItemDetails(ft.Container):
    
    def __init__(self):
        super(ItemDetails, self).__init__()
        
        self.content = ft.ExpansionPanelList([
            ft.ExpansionPanel(
                header=ft.Row([
                    ft.Text('video downloading (online-video-cutter.com).mp4')
                ]),
                content=ft.Row([
                    ft.Text('Content')
                ])
            )
        ])

class MainView(ft.View):
    
    def __init__(self, page:ft.Page):
        super(MainView, self).__init__()
        
        self.route = '/'
        self.page = page
        
        self.controls = [
            TitleBar(self.page),
            ItemDetails(),
        ]
        
        