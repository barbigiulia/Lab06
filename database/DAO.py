from database.DB_connect import DBConnect
from model.retailer import Retailer
from model.vendita import Vendita


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnno():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query ="""select distinct YEAR(Date) as anno
                    from go_daily_sales gds 
                    order by anno
                """
        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row["anno"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getBrand():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct Product_brand as brand
                    from go_products gp 
                    order by brand
                    """
        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row["brand"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getRetailers():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select gr.Retailer_code , gr.Retailer_name , gr.`Type` , gr.Country 
                    from go_retailers gr  
                    order by gr.Retailer_name 
                        """
        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(
                Retailer(
                        row["Retailer_code"],
                        row["Retailer_name"],
                        row["Type"],
                        row["Country"])
                        )

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getTopVendite(anno, brand, retailer):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT gds.Date, gp.Product_brand,gds.Retailer_code, gds.Product_number,
                    (gds.Unit_sale_price * gds.Quantity) AS ricavo
                    FROM go_daily_sales gds
                    JOIN go_products gp ON gds.Product_number = gp.Product_number
                    WHERE YEAR(gds.Date) = COALESCE(%s, YEAR(gds.Date))
                    AND gp.Product_brand = COALESCE(%s, gp.Product_brand)
                    AND gds.Retailer_code = COALESCE(%s, gds.Retailer_code)
                    ORDER BY ricavo DESC
                    LIMIT 5;
                                """
        # COALESCE(value1, value2, value3...)
        # restituisce il primo valore diverso da null
        # se tutti sono null --> null
        # A volte l'utente può non selezionare niente --> quindi valore =NULL
        # quindi se l'utente non seleziona nulla, non si applica quel filtro.
        # % è il valore scelto dall'utente
        cursor.execute(query, (anno, brand, retailer))
        res = []
        for row in cursor:
            res.append(
                Vendita(
                    row["Date"],
                    row["ricavo"],
                    row["Retailer_code"],
                    row["Product_number"],
                    row["Product_brand"]
                )
            )

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAnalisiVendite(anno, brand, retailer):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT SUM(gds.Unit_sale_price * gds.Quantity) AS sommaRicavi, 
                    COUNT(*) as vendite, 
                    COUNT(distinct gds.Retailer_code) as numRetailers, 
                    COUNT(distinct gp.Product_number) as numProdotti
                    FROM go_daily_sales gds
                    JOIN go_products gp ON gds.Product_number = gp.Product_number
                    WHERE YEAR(gds.`Date`) = COALESCE(%s, YEAR(gds.`Date`))
                    AND gp.Product_brand = COALESCE(%s, gp.Product_brand)
                    AND gds.Retailer_code = COALESCE(%s, gds.Retailer_code)
                    """

        # A volte l'utente può non selezionare niente --> quindi valore =NULL
        # quindi se l'utente non seleziona nulla, non si applica quel filtro.
        # % è il valore scelto dall'utente
        cursor.execute(query, (anno, brand, retailer))
        row = cursor.fetchone() # una sola riga

        # dato che Dictionary=true --> ottengo un dizionario
        # { "sommaRicavi": 42738, "vendite": 5, ....}

        # se non ci sono risultati :
        # SUM() = None
        # COUNT() = 0
        if row["sommaRicavi"] is None:
            row["sommaRicavi"] = 0

        cursor.close()
        cnx.close()
        return row