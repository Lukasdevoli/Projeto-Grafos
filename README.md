# Projeto-Grafos ✅

Este projeto é uma pequena aplicação em Python para construir grafos (lista de adjacência) e visualizar a Árvore Geradora Mínima (AGM) usando o algoritmo de Prim.

## ✨ Recursos
- Interface gráfica com `customtkinter` e plot com `matplotlib` + `networkx`
- Adição de arestas com pesos (suporta atualização de peso para arestas duplicadas)
- Geração aleatória de grafos (configurável)
- Execução visual e animada do algoritmo de Prim (controlável por velocidade)
- Remoção de arestas individuais e exclusão completa do grafo
- Exibição do peso total da AGM

## 🧰 Dependências
- Python 3.8+
- customtkinter
- networkx
- matplotlib

Você pode instalar rapidamente as dependências com pip:

pip install customtkinter networkx matplotlib

> Observação: em alguns sistemas o `customtkinter` exige a versão adequada do `tkinter` (normalmente já vem no Python instalável no Windows).


## ▶️ Executando a aplicação

1. Abra um terminal no diretório do projeto (`caminho/para/Projeto-Grafos`).
2. Execute:

python main.py

A janela da aplicação abrirá e você poderá interagir conforme indicado abaixo.

## 📋 Como usar
- **Adicionar Aresta:** preencha `Vértice 1`, `Vértice 2` e `Peso` e clique em **Adicionar Aresta**. Se a aresta já existir, o peso será atualizado.
- **Gerar Aleatório:** gera um grafo conectável com vértices nomeados (A, B, C...) e número de arestas configurável.
- **Remover Aresta:** selecione uma aresta na lista lateral e clique em **Remover Aresta**.
- **Executar Prim:** selecione o vértice inicial no menu e clique em **Executar Prim** para ver a construção animada da AGM. O peso total será mostrado.
- **Velocidade da Animação:** ajuste o slider lateral para aumentar/diminuir o intervalo (ms) entre destaque de arestas durante a animação.
- **Excluir Grafo:** limpa todo o grafo atual.

## 💡 Dicas
- Use nomes simples para vértices (letras ou números). Não é permitida aresta de um vértice para ele mesmo (laço).
- A geração aleatória garante conectividade inicial para evitar grafos desconexos.

## 🛠️ Melhorias implementadas
- Boas práticas de UX: feedbacks, validações (laços, peso inválido), atualização/remoção de arestas.
- Controle de animação e seleção de vértice inicial.

## 📄 Licença
Este repositório é para fins educacionais. Sinta-se à vontade para explorar e melhorar o código.

---

Se quiser, posso:
- Adicionar testes unitários para `graph.py` (Prim e operação de arestas) ✅
- Adicionar opção de salvar/carregar grafos em JSON ✅
- Refatorar para separar visualização e lógica do grafo em módulos separados ✅

Diga qual opção prefere que eu implemente em seguida.

