import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.data)

class BinaryTree:
    def __init__(self):
        self.root = None

    # Inserção por Nível
    def insert_level_order(self, data):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
            return
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            if current_node.left is None:
                current_node.left = new_node
                return
            else:
                queue.append(current_node.left)
            if current_node.right is None:
                current_node.right = new_node
                return
            else:
                queue.append(current_node.right)

    # --- MÉTODO DE REMOÇÃO ---
    def remove(self, key_to_remove):
        if not self.root:
            return "Árvore vazia"

        key_node = None
        deepest_node = None
        q = deque([self.root])

        # Encontra o nó a ser removido e o nó mais profundo/à direita
        while q:
            temp = q.popleft()
            if temp.data == key_to_remove:
                key_node = temp
            if temp.left:
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)
        
        if key_node is None:
            return f"Nó com valor {key_to_remove} não encontrado."

        # 'temp' ao final do loop é o nó mais profundo
        deepest_node_data = temp.data
        
        # Apaga o nó mais profundo
        q = deque([self.root])
        while q:
            node = q.popleft()
            if node.left:
                if node.left == temp:
                    node.left = None
                    break
                q.append(node.left)
            if node.right:
                if node.right == temp:
                    node.right = None
                    break
                q.append(node.right)
        
        # Substitui o dado do nó a ser removido pelo dado do nó mais profundo
        key_node.data = deepest_node_data
        return f"Nó {key_to_remove} removido e substituído por {deepest_node_data}."

    # Travessias
    def get_inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, current_node, result):
        if current_node:
            self._inorder(current_node.left, result)
            result.append(current_node.data)
            self._inorder(current_node.right, result)
    
    
    def get_preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, current_node, result):
        if current_node:
            result.append(current_node.data)
            self._preorder(current_node.left, result)
            self._preorder(current_node.right, result)

    def get_postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, current_node, result):
        if current_node:
            self._postorder(current_node.left, result)
            self._postorder(current_node.right, result)
            result.append(current_node.data)

    def get_level_order(self):
        if not self.root:
            return []
        result = []
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            result.append(current_node.data)
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        return result

    # Classificações
    def _get_height(self, node):
        if node is None: return -1
        return 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _is_regular_recursive(self, node):
        if node is None: return True
        if (node.left is None and node.right is not None) or (node.left is not None and node.right is None): return False
        return self._is_regular_recursive(node.left) and self._is_regular_recursive(node.right)

    def _is_balanced_recursive(self, node):
        if node is None: return (True, -1)
        is_left_balanced, left_height = self._is_balanced_recursive(node.left)
        if not is_left_balanced: return (False, 0)
        is_right_balanced, right_height = self._is_balanced_recursive(node.right)
        if not is_right_balanced: return (False, 0)
        balanced = abs(left_height - right_height) <= 1
        height = 1 + max(left_height, right_height)
        return (balanced, height)

    def is_regular(self): return self._is_regular_recursive(self.root)
    def is_perfect(self):
        height = self._get_height(self.root)
        node_count = len(self.get_level_order())
        return node_count == (2**(height + 1) - 1)
    def is_complete(self):
        if self.root is None: return True
        queue = deque([self.root])
        found_first_gap = False
        while queue:
            node = queue.popleft()
            if node is None:
                found_first_gap = True
            else:
                if found_first_gap: return False
                queue.append(node.left)
                queue.append(node.right)
        return True
    def is_balanced(self):
        is_b, _ = self._is_balanced_recursive(self.root)
        return is_b
    def is_unbalanced(self): return not self.is_balanced()

    # --- MÉTODO PARA VISUALIZAÇÃO GRÁFICA ---
    def to_networkx(self):
        G = nx.DiGraph()
        if not self.root:
            return G
        q = deque([self.root])
        while q:
            node = q.popleft()
            if node is None: continue
            G.add_node(node.data)
            if node.left:
                G.add_edge(node.data, node.left.data)
                q.append(node.left)
            if node.right:
                G.add_edge(node.data, node.right.data)
                q.append(node.right)
        return G

# --- CLASSE PARA INTERFACE GRÁFICA  ---
class TreeGUI:
    def __init__(self, main_window):
        self.tree = BinaryTree()
        self.main_window = main_window
        main_window.title("Visualizador de Árvore Binária (Trabalho)")

        frm = ttk.Frame(main_window, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")

        # --- Linha de Input e Botões de Ação ---
        self.entry = ttk.Entry(frm, width=20)
        self.entry.grid(row=0, column=0, padx=(0,5), sticky="ew")
        self.insert_btn = ttk.Button(frm, text="Inserir por Nível", command=self.on_insert)
        self.insert_btn.grid(row=0, column=1, padx=5, sticky="ew")
        self.delete_btn = ttk.Button(frm, text="Remover", command=self.on_delete)
        self.delete_btn.grid(row=0, column=2, padx=5, sticky="ew")

        # --- Botões de Travessia ---
        self.inorder_btn = ttk.Button(frm, text="In-Order", command=self.show_inorder)
        self.inorder_btn.grid(row=1, column=0, pady=8, sticky="ew")
        self.preorder_btn = ttk.Button(frm, text="Pre-Order", command=self.show_preorder)
        self.preorder_btn.grid(row=1, column=1, pady=8, sticky="ew")
        self.postorder_btn = ttk.Button(frm, text="Post-Order", command=self.show_postorder)
        self.postorder_btn.grid(row=1, column=2, pady=8, sticky="ew")

        # --- Botões de Classificação e Visualização ---
        self.classify_btn = ttk.Button(frm, text="Classificar Árvore", command=self.on_classify)
        self.classify_btn.grid(row=2, column=0, columnspan=2, pady=8, sticky="ew")
        self.draw_btn = ttk.Button(frm, text="Desenhar Árvore", command=self.draw_tree_window)
        self.draw_btn.grid(row=2, column=2, pady=8, sticky="ew")
        
        # --- Área de Saída de Texto ---
        self.output = tk.Text(frm, height=10)
        self.output.grid(row=3, column=0, columnspan=3, pady=8, sticky="nsew")
        
        # Configuração para redimensionamento
        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_rowconfigure(0, weight=1)
        frm.grid_columnconfigure(0, weight=1)


    def _read_key(self):
        txt = self.entry.get().strip()
        if not txt: return None
        # Para o trabalho, vamos assumir inteiros para simplicidade
        try:
            return int(txt)
        except ValueError:
            return None

    def on_insert(self):
        key = self._read_key()
        if key is None:
            messagebox.showwarning("Valor inválido", "Digite um número inteiro válido.")
            return
        self.tree.insert_level_order(key)
        self.entry.delete(0, tk.END)
        self._update_output_with_level_order()

    def on_delete(self):
        key = self._read_key()
        if key is None:
            messagebox.showwarning("Valor inválido", "Digite um número inteiro válido.")
            return
        result_msg = self.tree.remove(key)
        messagebox.showinfo("Remoção", result_msg)
        self.entry.delete(0, tk.END)
        self._update_output_with_level_order()

    def show_inorder(self):
        res = self.tree.get_inorder()
        self._set_output("In-Order: " + " ".join(map(str,res)))

    def show_preorder(self):
        res = self.tree.get_preorder()
        self._set_output("Pre-Order: " + " ".join(map(str,res)))

    def show_postorder(self):
        res = self.tree.get_postorder()
        self._set_output("Post-Order: " + " ".join(map(str,res)))
        
    def on_classify(self):
        if not self.tree.root:
            self._set_output("Classificação: Árvore vazia.")
            return

        classifications = []
        if self.tree.is_complete(): classifications.append("Completa")
        if self.tree.is_perfect(): classifications.append("Perfeita")
        if self.tree.is_regular(): classifications.append("Regular")
        if self.tree.is_balanced(): classifications.append("Balanceada")
        if self.tree.is_unbalanced(): classifications.append("Desbalanceada")
        
        self._set_output("Classificação da Árvore:\n • " + "\n • ".join(classifications))

    def _update_output_with_level_order(self):
        res = self.tree.get_level_order()
        self._set_output("Estado Atual (Level-Order): " + " ".join(map(str,res)))

    def _set_output(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def draw_tree_window(self):
        if not self.tree.root:
            messagebox.showinfo("Desenhar Árvore", "A árvore está vazia.")
            return
            
        win = tk.Toplevel(self.main_window)
        win.title("Visualização Gráfica da Árvore")
        fig = plt.Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        G = self.tree.to_networkx()
        pos = hierarchy_pos(G, self.tree.root.data)
        nx.draw(G, pos=pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=16)
        
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {root:(xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    # Pega os filhos do nó atual no grafo
    children = list(G.successors(root))
    if not children:
        return pos
        
    dx = width / len(children) 
    nextx = xcenter - width/2 - dx/2
    for child in children:
        nextx += dx
        pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, 
                            vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                            parent=root)
    return pos

if __name__ == "__main__":
    window = tk.Tk()
    app = TreeGUI(window)
    window.mainloop()