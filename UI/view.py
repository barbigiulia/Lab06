import flet as ft


class View(ft.UserControl):
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
        self.dd_anno = None
        self.dd_brand = None
        self.dd_retailer = None
        # buttons
        self.btn_topVendite = None
        self.btn_analizzaVendite = None
        # list view
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analizza vendite", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW with some controls
        anni = [ft.dropdown.Option(key="", text="Nessun filtro")]
        for anno in self._controller.model.getAnno():
            opzione = ft.dropdown.Option(key=str(anno), text=str(anno))
            # key = valore interno
            # text = ciò che vedo nel menu
            anni.append(opzione)
        self.dd_anno = ft.Dropdown(label="anno", options=anni, on_change=self._controller.scegliAnno)

        brands = [ft.dropdown.Option(key="", text="Nessun filtro")]
        for brand in self._controller.model.getBrand():
            opzione = ft.dropdown.Option(key=str(brand), text=str(brand))
            brands.append(opzione)
        self.dd_brand = ft.Dropdown(label="brand", options=brands, on_change=self._controller.scegliBrand)

        retailers = [ft.dropdown.Option(key="", text="Nessun filtro")]
        for retailer in self._controller.model.getRetailers():  # chiama il model --> DAO
            opzione = ft.dropdown.Option(key=str(retailer.code),
                                         text=str(retailer.name),
                                         data=retailer,
                                         on_click=self._controller.scegliRetailer)  # chiama il controller
            # il controller salva la scelta selezionata dall'utente
            retailers.append(opzione)
        self.dd_retailer = ft.Dropdown(label="retailer", options=retailers)


        row1 = ft.Row(controls=[self.dd_anno, self.dd_brand, self.dd_retailer],
                      alignment = ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)
        # buttons ----------------------------------------------------------------------------------------
        self.btn_topVendite = ft.ElevatedButton(text="Top Vendite",
                                                on_click=self._controller.handle_topVendite)

        self.btn_analizzaVendite = ft.ElevatedButton(text="Analizza vendite",
                                                     on_click=self._controller.handle_analisiVendite)

        row2 = ft.Row([self.btn_topVendite, self.btn_analizzaVendite],
                      alignment = ft.MainAxisAlignment.CENTER)
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
