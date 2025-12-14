from dataclasses import dataclass


@dataclass
class Rifugio:
    id : int
    nome : str
    localita : str
    altitudine : int
    capienza : int
    aperto : int

    def __repr__(self):
        return f"[{self.id}] {self.nome} ({self.localita})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Rifugio)

    def __hash__(self):
        return hash(self.id)