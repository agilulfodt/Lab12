import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self.rifugi = DAO.read_all_rifugi()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        archi = DAO.get_archi_pesati(year)
        for arco in archi:
            self.G.add_edge(self.rifugi[arco[0]], self.rifugi[arco[1]], weight=arco[2])

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        edges = self.G.edges(data='weight')
        peso_minimo = min(edges, key=self.get_peso)[2]
        peso_massimo = max(edges, key=self.get_peso)[2]
        return peso_minimo, peso_massimo

    def get_peso(self, edge):
        return edge[2]

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        count_minori = 0
        count_maggiori = 0
        for edge in self.G.edges(data='weight'):
            if edge[2] < soglia:
                count_minori += 1
            if edge[2] > soglia:
                count_maggiori += 1
        return count_minori, count_maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def calcola_cammino_minimo(self, soglia: float) -> list[str] | None:
        '''
        Calcola il cammino minimo (almeno due archi) e restituisce la lista di stringhe che descrivono il cammino
        :param soglia: si considerano solo i cammini con peso maggiore della soglia
        :return: lista di stringhe
        '''

        self._best_path = []
        self._best_weight = float('inf')
        cammino = []

        for node in self.G.nodes():
            self._ricorsione(soglia, node, [node])

        for i in range(len(self._best_path)):
            try:
                u = self._best_path[i]
                v = self._best_path[i + 1]
            except IndexError:
                continue
            cammino.append(f"{u} -> {v} [{self.G[u][v]['weight']}]")
        return cammino

    def _ricorsione(self, soglia, start, path):
        path_weight = self.calcola_weight(path)
        if path_weight < self._best_weight and len(path) >= 3:
            self._best_weight = path_weight
            self._best_path = path.copy()
            return

        for node in self.G[start]:
            weight_arco = self.G[start][node]['weight']
            if node in path:
                continue
            if weight_arco <= soglia or weight_arco + path_weight > self._best_weight:
                continue

            path.append(node)
            self._ricorsione(soglia, node, path)
            path.pop()

    def calcola_weight(self, path):
        weight = 0
        for i in range(len(path)):
            try:
                weight += self.G[path[i]][path[i + 1]]['weight']
            except IndexError:
                continue
        return weight