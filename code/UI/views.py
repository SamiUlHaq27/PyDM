import flet as ft


class ToolBar(ft.Row):
    
    def __init__(self, page):
        super(ToolBar, self).__init__()
        
        self.page = page
        
        self.url_dialog = ft.AlertDialog(
            modal=True,
            content=ft.TextField(),
            actions=[
                ft.TextButton('Go', on_click=self.on_go_btn_clicked),
                ft.TextButton('Close', on_click=lambda e:self.page.close(self.url_dialog))
            ]
        )
        
        self.controls = [
            ft.TextButton(text='Add', icon=ft.icons.ADD, on_click=self.on_add_btn_clicked)
        ]
    
    def on_add_btn_clicked(self, e):
        self.page.open(self.url_dialog)
    
    def on_go_btn_clicked(self, e):
        print(self.url_dialog.content.value)
       
class ItemDetails(ft.Container):
    
    def __init__(self):
        super(ItemDetails, self).__init__()
        
        self.name = ft.Text('Filename.ext')
        self.speed = ft.Text('123.4kb/s')
        self.download_size = ft.Text('99MB')
        self.total_size = ft.Text('100MB')
        
        self.url = ft.Text('http://asdfsadfsda.asd')
        self.progress_bar = ft.ProgressBar(value=0.3)
        
        self.pause_btn = ft.TextButton('Pause')
        self.start_btn = ft.TextButton('Start')
        self.resume_btn = ft.TextButton('Resume')
        
        self.content = ft.ExpansionPanelList([
            ft.ExpansionPanel(
                header=ft.Column([
                        ft.Row([
                            self.name,
                            self.speed,
                            ft.Row([
                                self.download_size,
                                ft.Text('/'),
                                self.total_size
                            ]),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            self.start_btn,
                            self.pause_btn,
                            self.resume_btn,
                            ft.TextButton('Cancel')
                        ])
                ]),
                content=ft.Column([
                    ft.Row([
                        ft.Text('Url: '),
                        self.url
                    ]),
                    self.progress_bar
                ])
            )
        ])

class MainView(ft.View):
    
    def __init__(self, page:ft.Page):
        super(MainView, self).__init__()
        
        self.route = '/'
        self.page = page
        
        self.controls = [
            ToolBar(page),
            ft.Column([
                ItemDetails()
            ])
        ]
    
