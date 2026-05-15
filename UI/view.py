import flet as ft
from flet_core import MainAxisAlignment


class View():
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddBorough = None
        self._btnCreaGrafo = None
        self._btnAnalisiArchi= None
        self.txt_result = None
        self.txt_container = None


    def load_interface(self):
        # title
        self._title = ft.Text("NYC wifi hotspots", color="blue", size=24)
        self._page.controls.append(self._title)

        self._ddBorough = ft.Dropdown(label="Seleziona un borough (b)", options=self._controller.readDropDown())

        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handleCreaGrafo)

        row = ft.Row([self._ddBorough, self._btnCreaGrafo], alignment=MainAxisAlignment.CENTER)
        self._page.controls.append(row)

        self._btnAnalisiArchi = ft.ElevatedButton("Analisi Archi", on_click=self._controller.handleAnalisiArchi)
        self._page.controls.append(ft.Row([self._btnAnalisiArchi], alignment=MainAxisAlignment.CENTER))

        self._txtP = ft.TextField(label="Probabilità (p)", width=150)
        self._txtD = ft.TextField(label="Durata (d)", width=150)
        self._btnSimula = ft.ElevatedButton("Simula", on_click=self._controller.handleSimula)

        row2 = ft.Row([self._txtP, self._txtD, self._btnSimula], alignment=MainAxisAlignment.CENTER)
        self._page.controls.append(row2)
        # List View
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()


    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
