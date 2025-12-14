from database.DB_connect import DBConnect
from database.connessione import Connessione
from database.rifugio import Rifugio

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def get_archi_pesati(year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        archi = []
        difficolta = ['facile', 'media', 'difficile']
        fattori_difficolta = [1.0, 1.5, 2.0]
        cursor.execute('SELECT * FROM connessione')
        for row in cursor:
            connessione = Connessione(**row)
            if connessione.anno <= year:
                peso = float(connessione.distanza) * fattori_difficolta[difficolta.index(connessione.difficolta)]
                archi.append((connessione.id_rifugio1, connessione.id_rifugio2, peso))
        return archi

    @staticmethod
    def read_all_rifugi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        rifugi = {}
        cursor.execute('SELECT * FROM rifugio')
        for row in cursor:
            rifugi[row['id']] = Rifugio(**row)
        return rifugi

if __name__ == '__main__':
    print(DAO.get_archi_pesati(2000))