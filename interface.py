# interface.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
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
        frame_inputs.grid_columnconfigure((0,1,2,3,4,5,6), weight=0)

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

        # Seletor para vértice inicial (será atualizado dinamicamente)
        self.start_option = ctk.CTkOptionMenu(frame_inputs, values=[], width=120)
        self.start_option.grid(row=0, column=5, padx=10, pady=10)

        # Botão para gerar grafo aleatório
        self.botao_gerar = ctk.CTkButton(frame_inputs, text="🎲 Gerar Aleatório",
                                         command=self.gerar_aleatorio, fg_color="#ffa500", hover_color="#ffb84d")
        self.botao_gerar.grid(row=0, column=6, padx=10, pady=10)

        self.botao_excluir = ctk.CTkButton(frame_inputs, text="🗑️ Excluir Grafo",
                                           command=self.excluir_grafo, fg_color="#ff4c4c", hover_color="#ff7f7f")
        self.botao_excluir.grid(row=0, column=7, padx=10, pady=10)

        # Parâmetro de animação (ms)
        self.animation_delay = 500  # valor padrão em milissegundos

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

        # Botão para remover aresta selecionada
        self.botao_remover = ctk.CTkButton(frame_lateral, text="❌ Remover Aresta",
                                           command=self.remover_aresta, fg_color="#ff6b6b", hover_color="#ff8b8b")
        self.botao_remover.pack(padx=10, pady=(5, 10), fill="x")

        # Slider para ajustar velocidade da animação (ms)
        ctk.CTkLabel(frame_lateral, text="Velocidade da Animação (ms)",
                     font=ctk.CTkFont(size=12)).pack(padx=10, pady=(10, 2))
        self.speed_slider = ctk.CTkSlider(frame_lateral, from_=100, to=1200, number_of_steps=11, command=self._set_speed)
        self.speed_slider.set(self.animation_delay)
        self.speed_slider.pack(padx=10, pady=(0, 10), fill="x")

        self.speed_label = ctk.CTkLabel(frame_lateral, text=f"{self.animation_delay} ms")
        self.speed_label.pack(padx=10, pady=(0, 10))

        # Inicializa plot
        self.plotar_grafo()
        # Desativa botão Prim até que haja arestas
        self.botao_prim.configure(state='disabled')

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

        if u == v:
            messagebox.showerror("Erro!", "Não é permitido adicionar laços (u == v).")
            return

        # Detecta aresta duplicada: se já existir entre u e v atualiza o peso
        duplicada = False
        if u in self.grafo.vertices:
            for viz, p in self.grafo.vertices[u]:
                if viz == v:
                    duplicada = True
                    break

        if duplicada:
            # Atualiza todos os lugares onde a aresta aparece
            self.grafo.vertices[u] = [(x, peso) if x == v else (x, w) for x, w in self.grafo.vertices[u]]
            self.grafo.vertices[v] = [(x, peso) if x == u else (x, w) for x, w in self.grafo.vertices[v]]
            messagebox.showinfo("Atualizado", f"Aresta {u} - {v} atualizada para peso {peso}.")

            # Atualiza listbox: procura e substitui a linha correspondente
            for i in range(self.lista_arestas.size()):
                txt = self.lista_arestas.get(i)
                if txt.startswith(f"{u} – {v} (") or txt.startswith(f"{v} – {u} ("):
                    self.lista_arestas.delete(i)
                    self.lista_arestas.insert(i, f"{u} – {v} (peso {peso})")
                    break
        else:
            # Adiciona ao grafo (graph.py)
            self.grafo.adicionar_aresta(u, v, peso)
            self.lista_arestas.insert(tk.END, f"{u} – {v} (peso {peso})")

        # Debug no console
        print(f"[DEBUG][Interface] Aresta adicionada/atualizada: {u} --({peso})-- {v}")
        print(f"[DEBUG][Interface] Grafo atual: {self.grafo.vertices}")

        # Limpa campos
        self.v1_entry.delete(0, 'end')
        self.v2_entry.delete(0, 'end')
        self.peso_entry.delete(0, 'end')
        self.master.focus()
        self.peso_total_label.configure(text="0")

        # Atualiza visual e controles
        self._update_start_option()
        self.botao_prim.configure(state="normal")
        self.plotar_grafo()

    def executar_prim(self):
        
        if not self.grafo.vertices:
            messagebox.showerror("Erro!", "O grafo está vazio.")
            return

        print("[DEBUG][Interface] Executando algoritmo de Prim...")
        print(f"[DEBUG][Interface] Grafo antes do Prim: {self.grafo.vertices}")

        inicio = self.start_option.get() if self.start_option.get() else list(self.grafo.vertices.keys())[0]
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
        self._update_start_option()
        self.botao_prim.configure(state="disabled")
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

        
        self.master.after(self.animation_delay, self._animar_arestas, mst, G, pos, ax, 0)

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

       
        self.master.after(self.animation_delay, self._animar_arestas, mst, G, pos, ax, index + 1)

    def remover_aresta(self):
        sel = self.lista_arestas.curselection()
        if not sel:
            messagebox.showinfo("Info", "Selecione uma aresta para remover.")
            return

        idx = sel[0]
        txt = self.lista_arestas.get(idx)
        # Formato esperado: "u – v (peso p)"
        try:
            parte = txt.split('(')[0].strip()
            u, v = [x.strip() for x in parte.split('–')]
        except Exception:
            messagebox.showerror("Erro", "Formato de aresta inválido.")
            return

        # Remove das estruturas do grafo
        if u in self.grafo.vertices:
            self.grafo.vertices[u] = [t for t in self.grafo.vertices[u] if t[0] != v]
            if not self.grafo.vertices[u]:
                del self.grafo.vertices[u]
        if v in self.grafo.vertices:
            self.grafo.vertices[v] = [t for t in self.grafo.vertices[v] if t[0] != u]
            if not self.grafo.vertices[v]:
                del self.grafo.vertices[v]

        self.lista_arestas.delete(idx)
        self.plotar_grafo()
        self._update_start_option()
        messagebox.showinfo("OK", f"Aresta {u} - {v} removida.")

    def gerar_aleatorio(self):
        n = simpledialog.askinteger("Gerar Grafo", "Número de vértices (3-12):", minvalue=3, maxvalue=12)
        if not n:
            return
        m = simpledialog.askinteger("Gerar Grafo", "Número de arestas (>= n-1):", minvalue=n-1, maxvalue=n*(n-1)//2)
        if not m:
            return

        # Gera nomes de vértices como letras
        letras = [chr(ord('A') + i) for i in range(n)]
        self.grafo = Grafo()
        self.lista_arestas.delete(0, tk.END)

        # Começa criando uma árvore para garantir conectividade
        for i in range(1, n):
            u = letras[i]
            v = random.choice(letras[:i])
            peso = round(random.uniform(1, 20), 2)
            self.grafo.adicionar_aresta(u, v, peso)
            self.lista_arestas.insert(tk.END, f"{u} – {v} (peso {peso})")

        # Adiciona arestas adicionais aleatórias
        extra = m - (n - 1)
        possiveis = []
        for i in range(n):
            for j in range(i+1, n):
                possiveis.append((letras[i], letras[j]))
        random.shuffle(possiveis)
        i = 0
        while extra > 0 and i < len(possiveis):
            u, v = possiveis[i]
            # Evita duplicatas
            exists = any(x[0] == v for x in self.grafo.vertices.get(u, []))
            if not exists:
                peso = round(random.uniform(1, 20), 2)
                self.grafo.adicionar_aresta(u, v, peso)
                self.lista_arestas.insert(tk.END, f"{u} – {v} (peso {peso})")
                extra -= 1
            i += 1

        self._update_start_option()
        self.botao_prim.configure(state="normal")
        self.plotar_grafo()

    def _update_start_option(self):
        vals = sorted(self.grafo.vertices.keys())
        if not vals:
            self.start_option.configure(values=[""], command=None)
            self.start_option.set("")
            return
        self.start_option.configure(values=vals)
        # Define preferencialmente o primeiro vértice
        self.start_option.set(vals[0])

    def _set_speed(self, value):
        try:
            self.animation_delay = int(float(value))
            self.speed_label.configure(text=f"{self.animation_delay} ms")
        except Exception:
            pass


if __name__ == "__main__":
    root = ctk.CTk()
    app = Interface(root)
    root.mainloop()
