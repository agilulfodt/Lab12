from typing import Any

import networkx as nx
from database.dao import DAO
import random

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
        metodo = 1#random.randint(1,2)
        self._best_path = []
        self._best_weight = float('inf')
        cammino = []
        if metodo == 1: #metodo di ricorsione
            for node in self.G.nodes():
                self._ricorsione(soglia, node, [node], self._best_weight)

            for index, node in enumerate(self._best_path):
                cammino.append(f"{node} -> {self._best_path[index + 1]}")

        # if metodo == 2:
        #     fw = nx.floyd_warshall(self.G, weight='weight')
        #     paths_lenghts = {a: dict(b) for a, b in fw.items()}
        #     for node1 in paths_lenghts:
        #         for node2 in paths_lenghts[node1]:
        #             if node1 != node2 and paths_lenghts[node1][node2] < self._best_weight:
        #                 sp = nx.shortest_path(self.G, source=node1, target=node2)
        #                 if len(sp) >= 3:
        #                     for i in range(len(sp)):
        return cammino

    def _ricorsione(self, soglia, start, path, weight):
        if weight < self._best_weight and len(path) >= 3:
            self._best_weight = weight
            self._best_path = path.copy()

        for node in self.G[start]:
            weight_attuale = self.G[start][node]['weight']
            if weight_attuale <= soglia:
                continue
            if weight + weight_attuale >= self._best_weight:
                continue
            if node in path:
                continue

            path.append(node)
            self._ricorsione(soglia, node, path, weight + weight_attuale)
            path.pop()