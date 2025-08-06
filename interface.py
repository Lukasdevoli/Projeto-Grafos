import tkinter as tk
from tkinter import messagebox
from graph import Grafo
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Árvore Geradora Mínima (Prim)")
        self.grafo = Grafo()

        # Inputs
        tk.Label(master, text="Vértice 1").grid(row=0, column=0)
        tk.Label(master, text="Vértice 2").grid(row=0, column=1)
        tk.Label(master, text="Peso").grid(row=0, column=2)

        self.v1_entry = tk.Entry(master)
        self.v2_entry = tk.Entry(master)
        self.peso_entry = tk.Entry(master)

        self.v1_entry.grid(row=1, column=0)
        self.v2_entry.grid(row=1, column=1)
        self.peso_entry.grid(row=1, column=2)

        tk.Button(master, text="Adicionar Aresta", command=self.adicionar).grid(row=1, column=3)
        tk.Button(master, text="Executar Prim", command=self.executar_prim).grid(row=2, column=0, columnspan=2)

        # Área do gráfico
        self.figura = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figura, master)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=4)

    def adicionar(self):
        u = self.v1_entry.get()
        v = self.v2_entry.get()
        try:
            peso = float(self.peso_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Peso inválido")
            return
        self.grafo.adicionar_aresta(u, v, peso)
        messagebox.showinfo("Sucesso", f"Aresta {u}-{v} com peso {peso} adicionada")
        self.v1_entry.delete(0, tk.END)
        self.v2_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)
        self.plotar_grafo()

    def executar_prim(self):
        if not self.grafo.vertices:
            messagebox.showerror("Erro", "Grafo vazio")
            return
        inicio = list(self.grafo.vertices.keys())[0]
        mst, total = self.grafo.prim(inicio)
        self.plotar_grafo(mst)
        messagebox.showinfo("Resultado", f"Peso total da árvore geradora mínima: {total}")

    def plotar_grafo(self, mst=None):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        G = nx.Graph()

        for u in self.grafo.vertices:
            for v, peso in self.grafo.vertices[u]:
                G.add_edge(u, v, weight=peso)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, ax=ax, node_color="lightblue", edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, ax=ax)

        if mst:
            mst_edges = [(u, v) for u, v, _ in mst]
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', width=2, ax=ax)

        self.canvas.draw()
