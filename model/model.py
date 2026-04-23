from database.DAO import DAO

class Model:
    def __init__(self):
        pass

    def getAnno(self):
        return DAO.getAnno()    # riempe il menu a tendina "anno"

    def getBrand(self):
        return DAO.getBrand()  # riempe il menu a tendina "brand"

    def getRetailers(self):
        return DAO.getRetailers()

    def getTopVendite(self, anno , brand, retailer):
        return DAO.getTopVendite(anno, brand, retailer)

    def getAnalisiVendite(self, anno , brand, retailer):
        return DAO.getAnalisiVendite(anno, brand, retailer)