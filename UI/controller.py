import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._Borough = None

    def readDropDown(self):
        boroughs=  self._model.readBoroughs()
        res =[]
        for b in boroughs:
            res.append(ft.dropdown.Option(b))   # lista di opzioni
        return res



    def handleCreaGrafo(self, e):
        borough = self._view._ddBorough.value
        print(f"Borough selezionato: {borough}")  # debug

        if borough is None or borough == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un Borough (b) ", color="red"))
            self._view.update_page()
            return


        # COSTRUISCO IL GRAFO
        print("Inizio buildGraph...")  # debug
        self._model.buildGraph(borough)
        print(f"Nodi: {self._model.getNumNodi()}, Archi: {self._model.getNumArchi()}")  # debug

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumNodi()} nodi"
                                                      f" e {self._model.getNumArchi()} archi", color="blue"))

        self._view.update_page()


    def handleAnalisiArchi(self, e):
        archiMaggiori = self._model.ArchiPesoMaggiore()  # SONO DELLE TUPLE !!!

        for n1, n2, peso in archiMaggiori:  # non serve più (data=True)
            # PESO è GIA' UN INTERO!!
            self._view.txt_result.controls.append(ft.Text(f"Arco ({n1}, {n2}) - peso {peso}", color="purple"))

        self._view.update_page()

    def handleSimula(self, e):
        try:
            p = float(self._view._txtP.value)
            d = int(self._view._txtD.value)
        except ValueError:
            self._view.create_alert("Inserire valori validi per p e d")
            return

        if p < 0.2 or p > 0.9:
            self._view.create_alert("p deve essere compreso tra 0.2 e 0.9")
            return
        if d <= 0:
            self._view.create_alert("d deve essere un intero positivo")
            return

        contatori = self._model.runSimulation(p, d)

        self._view.txt_result.controls.clear()
        for nta, count in contatori.items():
            self._view.txt_result.controls.append(
                ft.Text(f"NTA: {nta} → file condivisi: {count}", color="blue")
            )
        self._view.update_page()