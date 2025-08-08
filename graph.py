import heapq

class Grafo:
    def __init__(self):
        # Dicionário que armazena o grafo como lista de adjacência
        self.vertices = {}

    def adicionar_aresta(self, u, v, peso):
        """Adiciona uma aresta entre u e v com determinado peso"""
        if u not in self.vertices:
            self.vertices[u] = []
        if v not in self.vertices:
            self.vertices[v] = []
        self.vertices[u].append((v, peso))
        self.vertices[v].append((u, peso))  # Grafo não direcionado

    def prim(self, inicio):
        """Executa o algoritmo de Prim para gerar a árvore mínima"""
        print(f"\n[DEBUG][Prim] Iniciando no vértice: {inicio}")

        visitados = set()
        fila = []  # Fila de prioridade (min-heap)
        mst = []   # Lista da Árvore Geradora Mínima
        total = 0  # Peso total da AGM

        # Marca o vértice inicial como visitado
        visitados.add(inicio)
        print(f"[DEBUG][Prim] Visitados: {visitados}")

        # Adiciona as arestas do vértice inicial na fila
        for vizinho, peso in self.vertices[inicio]:
            print(f"[DEBUG][Prim] Adicionando aresta inicial: {inicio} --({peso})-- {vizinho}")
            heapq.heappush(fila, (peso, inicio, vizinho))

        # Enquanto houver arestas na fila
        while fila:
            peso, u, v = heapq.heappop(fila)
            print(f"[DEBUG][Prim] Analisando aresta: {u} --({peso})-- {v}")

            if v not in visitados:
                # Adiciona o vértice e a aresta à MST
                visitados.add(v)
                mst.append((u, v, peso))
                total += peso
                print(f"[DEBUG][Prim] Adicionada à MST: {u} --({peso})-- {v}")
                print(f"[DEBUG][Prim] Visitados agora: {visitados}")
                print(f"[DEBUG][Prim] Total acumulado: {total}")

                # Adiciona novas arestas saindo de v
                for viz, p in self.vertices[v]:
                    if viz not in visitados:
                        print(f"[DEBUG][Prim] Adicionando na fila: {v} --({p})-- {viz}")
                        heapq.heappush(fila, (p, v, viz))

        print(f"[DEBUG][Prim] FIM → MST final: {mst}")
        print(f"[DEBUG][Prim] Peso total: {total}\n")
        return mst, total
