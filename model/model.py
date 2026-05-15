import random

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self.grafo = nx.Graph() # NON ORIENTATO


    def readBoroughs(self):
        return DAO.getBorough()


    def buildGraph(self, b):
        nodi = DAO.getNodes(b)
        self.grafo.add_nodes_from(nodi)
        self.addEdges()

    def addEdges(self):
        NTA_nodes = self.grafo.nodes()    # [BK60, ...]
        archi = set()
        for nta1 in NTA_nodes:
            for nta2 in NTA_nodes:
                if nta1 == nta2:
                    continue
                key = frozenset({nta1, nta2})  #(a,b)==(b,a)
                if key in archi:
                    continue # se ho già aggiunto questo arco, passo all'iterazione successiva
                archi.add(key)

                SSID1 = set(DAO.getSSID(nta1))  # ottengo gli SSID per questo specifico nodo NTA
                SSID2 = set(DAO.getSSID(nta2))
                peso = len(SSID1|SSID2)  # UNIONE TRA DUE INSIEMI  (mi assicuro di convertire le liste in set)


                if peso > 0:
                   self.grafo.add_edge(nta1, nta2, weight=peso)


    def ArchiPesoMaggiore(self):

        somma = 0
        for nta1, nta2, dati in self.grafo.edges(data=True):
            peso = dati["weight"]
            somma+=int(peso)

        media = somma/len(self.grafo.edges)

        res = []
        for nta1, nta2, dati in self.grafo.edges(data=True):
            peso = dati["weight"]
            if int(peso) >media:
                res.append((nta1, nta2, peso))
        res.sort(key=lambda x: x[2], reverse=True)
        return res





    # =================
    # STATISTICHE GRAFO
    # ==================
    def getNumNodi(self):
        return len(self.grafo.nodes)

    def getNumArchi(self):
        return len(self.grafo.edges)



    # punto 2 esame

    def runSimulation(self, p, d):
        # contatore dei file per ogni NTA
        contatore = {nta:0 for nta in self.grafo.nodes()}

        # file attivi : lista di dizionari del tipo {nta, giorni_rimanenti}
        file_attivi = []
        for gg in range(100):
            # con una probabilità = p , aggiungo un nuovo file
            if random.random() < p:
                nta_casuale = random.choice(list(self.grafo.nodes()))
                file_attivi.append({"nta": nta_casuale, "durata": d})
                contatore[nta_casuale] += 1

            # regola C: propaga i file esistente nel vicino con peso maggiore
            nuovi_file = []
            nta_occupati = {}
            for f in file_attivi:
                nta_occupati[f["nta"]] = f

            for file in file_attivi:
                nuova_durata = file["durata"]//2
                if nuova_durata ==0:
                    continue # non si propaga più

                # trovo il vicino con peso maggiore senza file
                vicini = self.grafo[file["nta"]]   # {nta_vicino: {"weight": peso}}
                migliore = None
                peso_max = -1
                for vicino, dati in vicini.items():
                    if vicino not in nta_occupati and dati["weight"] >peso_max:
                        migliore = vicino
                        peso_max = dati["weight"]


                if migliore is not None:
                    nuovi_file.append({"nta": migliore, "durata": nuova_durata})
                    contatore[migliore] += 1
                    nta_occupati[migliore] = {"nta": migliore, "durata": nuova_durata}

            file_attivi.extend(nuovi_file)

            # decremento o rimuovo quelli scaduti
            for file in file_attivi:
                file["durata"] -= 1
            file_attivi = [f for f in file_attivi if f["durata"] > 0]

        return  contatore