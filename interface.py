import customtkinter as ctk
from tkinter import messagebox
from graph import Grafo
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Interface:
    def __init__(self, master):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.master = master
        self.master.title("Árvore Geradora Mínima (Prim)")
        self.master.geometry("800x600")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.grafo = Grafo()

        # Frame de entrada
        self.frame_topo = ctk.CTkFrame(master)
        self.frame_topo.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.v1_entry = ctk.CTkEntry(self.frame_topo, placeholder_text="Vértice 1")
        self.v2_entry = ctk.CTkEntry(self.frame_topo, placeholder_text="Vértice 2")
        self.peso_entry = ctk.CTkEntry(self.frame_topo, placeholder_text="Peso")

        self.v1_entry.grid(row=0, column=0, padx=5, pady=5)
        self.v2_entry.grid(row=0, column=1, padx=5, pady=5)
        self.peso_entry.grid(row=0, column=2, padx=5, pady=5)

        self.botao_adicionar = ctk.CTkButton(self.frame_topo, text="Adicionar Aresta", command=self.adicionar)
        self.botao_adicionar.grid(row=0, column=3, padx=10)

        self.botao_prim = ctk.CTkButton(self.frame_topo, text="Executar Prim", command=self.executar_prim)
        self.botao_prim.grid(row=0, column=4, padx=10)

        self.botao_limpar = ctk.CTkButton(self.frame_topo, text="Limpar Grafo", command=self.limpar_grafo)
        self.botao_limpar.grid(row=0, column=5, padx=10)


        # Frame do gráfico
        self.frame_grafo = ctk.CTkFrame(master)
        self.frame_grafo.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.frame_grafo.grid_rowconfigure(0, weight=1)
        self.frame_grafo.grid_columnconfigure(0, weight=1)

        self.figura = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafo)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

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
        self.v1_entry.delete(0, 'end')
        self.v2_entry.delete(0, 'end')
        self.peso_entry.delete(0, 'end')
        self.plotar_grafo()

    def executar_prim(self):
        if not self.grafo.vertices:
            messagebox.showerror("Erro", "Grafo vazio")
            return
        inicio = list(self.grafo.vertices.keys())[0]
        mst, total = self.grafo.prim(inicio)
        self.plotar_grafo(mst)
        messagebox.showinfo("Resultado", f"Peso total da árvore geradora mínima: {total}")

    def limpar_grafo(self):
        self.grafo.vertices.clear()
        self.plotar_grafo()
        messagebox.showinfo("Limpo", "Grafo apagado com sucesso!")

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
