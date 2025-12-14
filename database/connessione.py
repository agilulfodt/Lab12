from dataclasses import dataclass
import datetime


@dataclass
class Connessione:
    id : int
    id_rifugio1 : int
    id_rifugio2 : int
    distanza : float
    difficolta : str
    durata : datetime.timedelta
    anno : int

    def __repr__(self):
        return f"Connessione({self.id} da {self.id_rifugio1} a {self.id_rifugio2})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Connessione)

    def __hash__(self):
        return hash(self.id)