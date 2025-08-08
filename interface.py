# interface.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from graph import Grafo
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class Interface:
    def __init__(self, master):
        # Aparência do customtkinter
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.master = master
        self.master.title("Árvore Geradora Mínima (Prim)")
        self.master.geometry("1100x700")

        # Grid responsivo principal
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # Instância do grafo
        self.grafo = Grafo()

        #  Frame de Inputs 
        frame_inputs = ctk.CTkFrame(master, fg_color="#fff7d6", corner_radius=10)
        frame_inputs.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        frame_inputs.grid_columnconfigure((0,1,2,3,4,5), weight=0)

        self.v1_entry = ctk.CTkEntry(frame_inputs, placeholder_text="Vértice 1", width=120)
        self.v1_entry.grid(row=0, column=0, padx=10, pady=10)

        self.v2_entry = ctk.CTkEntry(frame_inputs, placeholder_text="Vértice 2", width=120)
        self.v2_entry.grid(row=0, column=1, padx=10, pady=10)

        self.peso_entry = ctk.CTkEntry(frame_inputs, placeholder_text="Peso", width=120)
        self.peso_entry.grid(row=0, column=2, padx=10, pady=10)

        # Botões principais
        self.botao_adicionar = ctk.CTkButton(frame_inputs, text="➕ Adicionar Aresta",
                                             command=self.adicionar, fg_color="#2e8b57", hover_color="#3a9a6a")
        self.botao_adicionar.grid(row=0, column=3, padx=10, pady=10)

        self.botao_prim = ctk.CTkButton(frame_inputs, text="🚀 Executar Prim",
                                        command=self.executar_prim, fg_color="#1e90ff", hover_color="#4aa0ff")
        self.botao_prim.grid(row=0, column=4, padx=10, pady=10)

        self.botao_excluir = ctk.CTkButton(frame_inputs, text="🗑️ Excluir Grafo",
                                           command=self.excluir_grafo, fg_color="#ff4c4c", hover_color="#ff7f7f")
        self.botao_excluir.grid(row=0, column=5, padx=10, pady=10)

        # Frame do Gráfico
        frame_grafico = ctk.CTkFrame(master, fg_color="#c4fff9", corner_radius=10)
        frame_grafico.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame_grafico.grid_rowconfigure(0, weight=1)
        frame_grafico.grid_columnconfigure(0, weight=1)

        # Figura matplotlib
        self.figura = plt.Figure(figsize=(7, 5), dpi=100, facecolor='#c4fff9')
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Painel Lateral 
        frame_lateral = ctk.CTkFrame(master, fg_color="#e7ffb0", corner_radius=10, width=250)
        frame_lateral.grid(row=1, column=1, padx=10, pady=10, sticky="ns")
        frame_lateral.grid_propagate(False)

        ctk.CTkLabel(frame_lateral, text="Arestas Adicionadas",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(padx=10, pady=(10, 5))

        # Listbox para mostrar arestas adicionadas
        self.lista_arestas = tk.Listbox(frame_lateral, width=30, height=15, font=("Arial", 11),
                                        bg="#f9f9f9", fg="black", relief="sunken", borderwidth=1,
                                        selectbackground="#1e90ff", selectforeground="white")
        self.lista_arestas.pack(padx=10, pady=5, fill="y", expand=True)

        ctk.CTkLabel(frame_lateral, text="Peso Total da AGM",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(padx=10, pady=(10, 5))

        self.peso_total_label = ctk.CTkLabel(frame_lateral, text="0",
                                             font=ctk.CTkFont(size=16, weight="bold"),
                                             fg_color="#f9f9f9", text_color="black", corner_radius=8, height=30)
        self.peso_total_label.pack(padx=10, pady=(5, 10), fill="x")

        # Inicializa plot
        self.plotar_grafo()

    # Funções da Interface 
    def adicionar(self):
      
        u = self.v1_entry.get().strip()
        v = self.v2_entry.get().strip()
        try:
            peso = float(self.peso_entry.get())
        except ValueError:
            messagebox.showerror("Erro!", "O valor do peso é inválido.")
            return

        if not u or not v:
            messagebox.showerror("Erro!", "Os campos dos vértices não podem estar vazios.")
            return

        # Adiciona ao grafo (graph.py)
        self.grafo.adicionar_aresta(u, v, peso)

        # Debug no console
        print(f"[DEBUG][Interface] Aresta adicionada: {u} --({peso})-- {v}")
        print(f"[DEBUG][Interface] Grafo atual: {self.grafo.vertices}")

        # Atualiza lista lateral e limpa campos
        self.lista_arestas.insert(tk.END, f"{u} – {v} (peso {peso})")
        self.v1_entry.delete(0, 'end')
        self.v2_entry.delete(0, 'end')
        self.peso_entry.delete(0, 'end')
        self.master.focus()
        self.peso_total_label.configure(text="0")
        self.plotar_grafo()

    def executar_prim(self):
        
        if not self.grafo.vertices:
            messagebox.showerror("Erro!", "O grafo está vazio.")
            return

        print("[DEBUG][Interface] Executando algoritmo de Prim...")
        print(f"[DEBUG][Interface] Grafo antes do Prim: {self.grafo.vertices}")

        inicio = list(self.grafo.vertices.keys())[0]
        mst, total = self.grafo.prim(inicio)

        # Mostra total na interface e em debug
        self.peso_total_label.configure(text=f"{total:.2f}")
        print(f"[DEBUG][Interface] MST retornada: {mst}")
        print(f"[DEBUG][Interface] Peso total retornado: {total}")

        # Anima a construção da MST (destaca arestas)
        self.plotar_grafo_animado(mst)

    def excluir_grafo(self):
      
        if not self.grafo.vertices:
            messagebox.showinfo("Info", "O grafo já está vazio.")
            return

        # Substitui por novo grafo vazio
        self.grafo = Grafo()
        self.lista_arestas.delete(0, tk.END)
        self.peso_total_label.configure(text="0")
        self.plotar_grafo()
        print("[DEBUG][Interface] Grafo excluído.")
        messagebox.showinfo("OK", "O grafo foi excluído.")

    # ----------------- Plotagem estática -----------------
    def plotar_grafo(self, mst=None):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        ax.set_title("Visualização do Grafo", fontsize=14, color="#333333")
        ax.set_facecolor('#c4fff9')
        self.figura.patch.set_facecolor('#c4fff9')

        # Monta o NetworkX Graph a partir da lista de adjacência
        G = nx.Graph()
        for u, arestas in self.grafo.vertices.items():
            for v, peso in arestas:
                # add_edge em grafo não direcionado; se duplicar, NetworkX mantém 1 aresta
                G.add_edge(u, v, weight=peso)

        if len(G.nodes()) == 0:
            self.canvas.draw()
            return

        # Layout fixo por seed para manter posições estáveis
        pos = nx.spring_layout(G, seed=42, k=0.9)
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        node_colors = ["#ff7eb9", "#7afcff", "#feff9c", "#b28dff", "#ffb3ba"]

        nx.draw(G, pos, with_labels=True, ax=ax,
                node_color=[random.choice(node_colors) for _ in G.nodes],
                edge_color="#aaaaaa", node_size=1000, font_size=11, font_weight='bold',
                font_color="black", width=1.5)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='#555555', font_size=9, ax=ax)

        if mst:
            # Lista de arestas (u,v) da MST — desenha em destaque
            mst_edges = [(u, v) for u, v, _ in mst]
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=mst_edges, edge_color='#ff4c4c', width=3.0)

        self.canvas.draw()

   
    def plotar_grafo_animado(self, mst):
       
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        ax.set_title("Construindo a Árvore Geradora Mínima...", fontsize=14, color="#333333")
        ax.set_facecolor('#c4fff9')
        self.figura.patch.set_facecolor('#c4fff9')

        G = nx.Graph()
        for u, arestas in self.grafo.vertices.items():
            for v, peso in arestas:
                G.add_edge(u, v, weight=peso)

        if len(G.nodes()) == 0:
            self.canvas.draw()
            return

        pos = nx.spring_layout(G, seed=42, k=0.9)
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        node_colors = ["#ff7eb9", "#7afcff", "#feff9c", "#b28dff", "#ffb3ba"]

        # Desenha grafo base (arestas em cinza)
        nx.draw(G, pos, with_labels=True, ax=ax,
                node_color=[random.choice(node_colors) for _ in G.nodes],
                edge_color="#cccccc", node_size=1000, font_size=11, font_weight='bold',
                font_color="black", width=1.5)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='#555555', font_size=9, ax=ax)

        self.canvas.draw()

        
        self.master.after(500, self._animar_arestas, mst, G, pos, ax, 0)

    def _animar_arestas(self, mst, G, pos, ax, index):
      
        if index >= len(mst):
            ax.set_title("AGM Finalizada!", fontsize=14, color="green")
            self.canvas.draw()
            return

        # Destaque da aresta atual
        u, v, peso = mst[index]
        print(f"[DEBUG][Anim] Destacando aresta {index+1}/{len(mst)}: {u} --({peso})-- {v}")
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color='#ff4c4c', width=3.0)
        self.canvas.draw()

       
        self.master.after(400, self._animar_arestas, mst, G, pos, ax, index + 1)



if __name__ == "__main__":
    root = ctk.CTk()
    app = Interface(root)
    root.mainloop()
