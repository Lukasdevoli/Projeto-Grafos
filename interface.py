import tkinter as tk
from tkinter import messagebox, ttk
from graph import Grafo
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Árvore Geradora Mínima (Prim)")
        self.master.configure(bg="#ffeef8")
        self.grafo = Grafo()
        self.arestas_adicionadas = []

        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        style.configure("TLabel", background="#ffeef8", font=("Arial", 11, "bold"))

        
        frame_inputs = tk.Frame(master, bg="#fff7d6", bd=3, relief="ridge")
        frame_inputs.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        tk.Label(frame_inputs, text="Vértice 1", bg="#fff7d6", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame_inputs, text="Vértice 2", bg="#fff7d6", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_inputs, text="Peso", bg="#fff7d6", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

        self.v1_entry = tk.Entry(frame_inputs, font=("Arial", 11), relief="solid", bd=1, bg="#ffffff")
        self.v2_entry = tk.Entry(frame_inputs, font=("Arial", 11), relief="solid", bd=1, bg="#ffffff")
        self.peso_entry = tk.Entry(frame_inputs, font=("Arial", 11), relief="solid", bd=1, bg="#ffffff")

        self.v1_entry.grid(row=1, column=0, padx=5, pady=5)
        self.v2_entry.grid(row=1, column=1, padx=5, pady=5)
        self.peso_entry.grid(row=1, column=2, padx=5, pady=5)

        # Botões
        tk.Button(frame_inputs, text="➕ Adicionar Aresta", command=self.adicionar,
        bg="#2e8b57", fg="white", font=("Arial", 11, "bold")).grid(row=1, column=3, padx=10)

        tk.Button(frame_inputs, text="🚀 Executar Prim", command=self.executar_prim,
        bg="#1e90ff", fg="white", font=("Arial", 11, "bold")).grid(row=2, column=0, columnspan=3, pady=10)

        tk.Button(frame_inputs, text="🗑️ Excluir Grafo", command=self.excluir_grafo,
        bg="#ff4c4c", fg="white", font=("Arial", 11, "bold")).grid(row=2, column=3, padx=10, pady=5)


        # Lista de arestas e peso total
        frame_lateral = tk.Frame(master, bg="#e7ffb0", bd=3, relief="ridge")
        frame_lateral.grid(row=1, column=1, padx=10, pady=5, sticky="n")

        tk.Label(frame_lateral, text="Arestas Adicionadas", bg="#e7ffb0", font=("Arial", 11, "bold")).pack(pady=5)
        self.lista_arestas = tk.Listbox(frame_lateral, width=25, height=10, font=("Arial", 10),
                                        bg="#ffffff", selectbackground="#ffb3ba")
        self.lista_arestas.pack(padx=5, pady=5)

        tk.Label(frame_lateral, text="Peso Total", bg="#e7ffb0", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        self.peso_total_label = tk.Label(frame_lateral, text="0", bg="#ffffff", fg="#333333",
        font=("Arial", 12, "bold"), width=20, relief="sunken", bd=1)
        self.peso_total_label.pack(pady=(0, 10))

        # Área do gráfico
        frame_grafico = tk.Frame(master, bg="#c4fff9", bd=3, relief="ridge")
        frame_grafico.grid(row=1, column=0, padx=10, pady=5)

        self.figura = plt.Figure(figsize=(7, 5), dpi=100, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.figura, frame_grafico)
        self.canvas.get_tk_widget().pack()

    def adicionar(self):
        u = self.v1_entry.get().strip()
        v = self.v2_entry.get().strip()
        try:
            peso = float(self.peso_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Peso inválido")
            return

        if u == "" or v == "":
            messagebox.showerror("Erro!", "Preencha todos os campos!")
            return

        self.grafo.adicionar_aresta(u, v, peso)
        self.arestas_adicionadas.append(f"{u} – {v} (peso {peso})")
        self.lista_arestas.insert(tk.END, f"{u} – {v} (peso {peso})")

        self.v1_entry.delete(0, tk.END)
        self.v2_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)

        self.plotar_grafo()
        self.peso_total_label.config(text="0")

    def executar_prim(self):
        if not self.grafo.vertices:
            messagebox.showerror("Erro!", "Grafo vazio!")
            return

        inicio = list(self.grafo.vertices.keys())[0]
        mst, total = self.grafo.prim(inicio)
        self.peso_total_label.config(text=str(total))
        self.plotar_grafo_animado(mst)

    def excluir_grafo(self):
        self.grafo = Grafo()
        self.arestas_adicionadas.clear()
        self.lista_arestas.delete(0, tk.END)
        self.peso_total_label.config(text="0")
        self.figura.clear()
        self.canvas.draw()
        messagebox.showinfo("Lixo","O grafo foi excluído.")

    def plotar_grafo(self, mst=None):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        ax.set_title(" Visualização do Grafo", fontsize=14, color="#333333", pad=20)
        ax.set_facecolor("#fdfdfd")

        G = nx.Graph()
        for u in self.grafo.vertices:
            for v, peso in self.grafo.vertices[u]:
                G.add_edge(u, v, weight=peso)

        pos = nx.spring_layout(G, seed=42)
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        node_colors = [random.choice(["#ff7eb9", "#7afcff", "#feff9c", "#b28dff", "#ffb3ba"]) for _ in G.nodes]

        nx.draw(G, pos, with_labels=True, ax=ax,
                node_color=node_colors, edge_color="#bbbbbb",
                node_size=900, font_size=10, font_weight='bold',
                font_color="black")

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9, ax=ax)

        if mst:
            mst_edges = [(u, v) for u, v, _ in mst]
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='#ff4c4c', width=2.5, ax=ax)

        self.canvas.draw()

    def plotar_grafo_animado(self, mst):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        ax.set_title("Visualização do Grafo", fontsize=14, color="#333333", pad=20)
        ax.set_facecolor("#fdfdfd")

        G = nx.Graph()
        for u in self.grafo.vertices:
            for v, peso in self.grafo.vertices[u]:
                G.add_edge(u, v, weight=peso)

        pos = nx.spring_layout(G, seed=42)
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        node_colors = [random.choice(["#ff7eb9", "#7afcff", "#feff9c", "#b28dff", "#ffb3ba"]) for _ in G.nodes]

        nx.draw(G, pos, with_labels=True, ax=ax,
                node_color=node_colors, edge_color="#cccccc",
                node_size=900, font_size=10, font_weight='bold', font_color="black")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9, ax=ax)

        self.canvas.draw()
        self.master.after(500, self._animar_arestas, mst, G, pos, ax, 0)

    def _animar_arestas(self, mst, G, pos, ax, index):
        if index >= len(mst):
            return

        u, v, _ = mst[index]
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='#ff4c4c', width=3, ax=ax)
        self.canvas.draw()
        self.master.after(400, self._animar_arestas, mst, G, pos, ax, index + 1)
