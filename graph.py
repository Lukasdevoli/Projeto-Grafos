import heapq

class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_aresta(self, u, v, peso):
        if u not in self.vertices:
            self.vertices[u] = []
        if v not in self.vertices:
            self.vertices[v] = []
        self.vertices[u].append((v, peso))
        self.vertices[v].append((u, peso))  # não direcionado

    def prim(self, inicio):
        visitados = set()
        fila = []
        mst = []
        total = 0

        visitados.add(inicio)
        for vizinho, peso in self.vertices[inicio]:
            heapq.heappush(fila, (peso, inicio, vizinho))

        while fila:
            peso, u, v = heapq.heappop(fila)
            if v not in visitados:
                visitados.add(v)
                mst.append((u, v, peso))
                total += peso # botar if 
                for viz, p in self.vertices[v]:
                    if viz not in visitados:
                        heapq.heappush(fila, (p, v, viz))

        return mst, total
