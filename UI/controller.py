import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._retailer = None

    @property
    def model(self):
        return self._model

    def scegliAnno(self, e):   # sempre l'evento passato come parametro
        anno = e.control.value
        print("Anno selezionato:", anno)  # SALVO LA SCELTA

    def scegliBrand(self, e):
        brand = e.control.value
        print("Brand selezionato:", brand)

    def scegliRetailer(self, e):
        self._retailer = e.control.data  # DIFFERENZA !!! TRA MVC E OOP
        print("Retailer selezionato:", self._retailer)

# METODI PER I BOTTONI
    def handle_topVendite(self,e):
        self._view.txt_result.controls.clear()
        # recupero l'ANNO e il BRAND
        anno = self._view.dd_anno.value
        if anno == "" or anno is None:
            anno = None
        else:
            anno = int(anno) # meglio passare a COALESCE un intero o None

        brand = self._view.dd_brand.value
        if brand == "" or brand is None:
            brand = None

        # l'oggetto Retailer è SALVATO NEL METODO Self, scegliReatailer()
        if self._retailer is not None:
            retailer = self._retailer.code  # recupero il codice
        else:
            retailer = None

        #chiamata al model
        topVendite = self._model.getTopVendite(anno, brand, retailer)

        #stampo i risultati
        if not topVendite:
            self._view.txt_result.controls.append(ft.Text("Nessuna vendita trovata"))
        else:
            for v in topVendite:
                self._view.txt_result.controls.append(ft.Text(str(v)))
        self._view.update_page()

    def handle_analisiVendite(self,e):
        self._view.txt_result.controls.clear()
        # recupero l'ANNO e il BRAND
        anno = self._view.dd_anno.value
        if anno == "" or anno is None:
            anno = None
        else:
            anno = int(anno)  # meglio passare a COALESCE un intero o None

        brand = self._view.dd_brand.value
        if brand == "" or brand is None:
            brand = None

        # l'oggetto Retailer è SALVATO NEL METODO Self, scegliReatailer()
        if self._retailer is not None:
            retailer = self._retailer.code  # recupero il codice
        else:
            retailer = None

        # dizionario
        statistiche = self._model.getAnalisiVendite(anno, brand, retailer)

        if statistiche is None:
            self._view.txt_result.controls.append(ft.Text("Nessun risultato trovato"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text("Statistiche vendite:"))
        self._view.txt_result.controls.append(ft.Text(f"Giro d'affari: {statistiche['sommaRicavi']}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero vendite: {statistiche['vendite']}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero retailers coinvolti: {statistiche['numRetailers']}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero prodotti coinvolti: {statistiche['numProdotti']}"))

        self._view.update_page()