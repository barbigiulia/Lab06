

import sqlite3

class DAO():
    DB_PATH = "database/nyc_wifi_hotspots.db"

    @staticmethod
    def getBorough():
        cnx = sqlite3.connect(DAO.DB_PATH)
        cnx.row_factory = sqlite3.Row
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT DISTINCT Borough 
            FROM nyc_wifi_hotspot_locations 
            ORDER BY Borough
        """)

        res = cursor.fetchall()
        cursor.close()
        cnx.close()
        return [row["Borough"] for row in res]

    @staticmethod
    def getNodes(b):
        cnx = sqlite3.connect(DAO.DB_PATH)
        cnx.row_factory = sqlite3.Row
        cursor = cnx.cursor()
        query = """
                select distinct nwhl.NTACode 
                from nyc_wifi_hotspot_locations nwhl 
                where nwhl.Borough = ?
            """
        cursor.execute(query, (b,))

        res = cursor.fetchall()
        cursor.close()
        cnx.close()
        risultati = []
        for row in res:
            risultati.append(row["NTACode"])
        return risultati

    @staticmethod
    def getSSID(ntaCode):
        cnx = sqlite3.connect(DAO.DB_PATH)
        cnx.row_factory = sqlite3.Row
        cursor = cnx.cursor()
        query = """
                select distinct nwhl.SSID 
                from nyc_wifi_hotspot_locations nwhl 
                where nwhl.NTACode =?
                """
        cursor.execute(query, (ntaCode,))

        res = cursor.fetchall()
        cursor.close()
        cnx.close()
        risultati = []
        for row in res:
            risultati.append(row["SSID"])
        return risultati