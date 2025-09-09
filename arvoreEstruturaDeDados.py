import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)
        return y

    def _balance(self, node):
        self.update_height(node)
        bf = self.balance_factor(node)

        if bf > 1:
            if self.balance_factor(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if bf < -1:
            if self.balance_factor(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return Node(key)
        if key == node.key:
            return node
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        return self._balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        return self._balance(node) if node else None

    def inorder(self):
        res = []
        self._inorder(self.root, res)
        return res

    def _inorder(self, node, res):
        if not node:
            return
        self._inorder(node.left, res)
        res.append(node.key)
        self._inorder(node.right, res)

    def preorder(self):
        res = []
        self._preorder(self.root, res)
        return res

    def _preorder(self, node, res):
        if not node:
            return
        res.append(node.key)
        self._preorder(node.left, res)
        self._preorder(node.right, res)

    def postorder(self):
        res = []
        self._postorder(self.root, res)
        return res

    def _postorder(self, node, res):
        if not node:
            return
        self._postorder(node.left, res)
        self._postorder(node.right, res)
        res.append(node.key)

    def to_levels_text(self):
        if not self.root:
            return "<árvore vazia>"
        q = deque([(self.root, 0)])
        levels = {}
        while q:
            node, lvl = q.popleft()
            levels.setdefault(lvl, []).append(str(node.key))
            if node.left:
                q.append((node.left, lvl+1))
            if node.right:
                q.append((node.right, lvl+1))
        lines = []
        for lvl in sorted(levels.keys()):
            lines.append(f"Nivel {lvl}: " + " ".join(levels[lvl]))
        return "\n".join(lines)

    def to_networkx(self):
        G = nx.DiGraph()
        if not self.root:
            return G
        q = deque([self.root])
        while q:
            node = q.popleft()
            G.add_node(node.key)
            if node.left:
                G.add_node(node.left.key)
                G.add_edge(node.key, node.left.key)
                q.append(node.left)
            if node.right:
                G.add_node(node.right.key)
                G.add_edge(node.key, node.right.key)
                q.append(node.right)
        return G

class TreeGUI:
    def __init__(self, root):
        self.tree = AVLTree()
        self.root = root
        root.title("Árvore AVL (BST) - Interface Gráfica")

        frm = ttk.Frame(root, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")

        self.entry = ttk.Entry(frm, width=20)
        self.entry.grid(row=0, column=0, padx=(0,5))
        self.insert_btn = ttk.Button(frm, text="Inserir", command=self.on_insert)
        self.insert_btn.grid(row=0, column=1, padx=5)
        self.delete_btn = ttk.Button(frm, text="Remover", command=self.on_delete)
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.inorder_btn = ttk.Button(frm, text="In-order", command=self.show_inorder)
        self.inorder_btn.grid(row=1, column=0, pady=(8,0))
        self.preorder_btn = ttk.Button(frm, text="Pre-order", command=self.show_preorder)
        self.preorder_btn.grid(row=1, column=1, pady=(8,0))
        self.postorder_btn = ttk.Button(frm, text="Post-order", command=self.show_postorder)
        self.postorder_btn.grid(row=1, column=2, pady=(8,0))

        self.textual_btn = ttk.Button(frm, text="Visualização textual", command=self.show_textual)
        self.textual_btn.grid(row=2, column=0, columnspan=2, pady=(8,0), sticky="ew")

        self.draw_btn = ttk.Button(frm, text="Desenhar árvore", command=self.draw_tree_window)
        self.draw_btn.grid(row=2, column=2, pady=(8,0))

        self.output = tk.Text(frm, width=50, height=10)
        self.output.grid(row=3, column=0, columnspan=3, pady=(8,0))

        self.fig = None
        self.canvas = None

    def _read_key(self):
        txt = self.entry.get().strip()
        if not txt:
            return None
        try:
            key = int(txt)
            return key
        except ValueError:
            try:
                key = float(txt)
                return key
            except ValueError:
                return None

    def on_insert(self):
        key = self._read_key()
        if key is None:
            messagebox.showwarning("Valor inválido", "Digite um número válido (int ou float).")
            return
        self.tree.insert(key)
        self.entry.delete(0, tk.END)
        self.show_textual(auto=True)

    def on_delete(self):
        key = self._read_key()
        if key is None:
            messagebox.showwarning("Valor inválido", "Digite um número válido (int ou float).")
            return
        self.tree.delete(key)
        self.entry.delete(0, tk.END)
        self.show_textual(auto=True)

    def show_inorder(self):
        res = self.tree.inorder()
        self._set_output("Em Ordem: " + " ".join(map(str,res)))

    def show_preorder(self):
        res = self.tree.preorder()
        self._set_output("Pre Ordem: " + " ".join(map(str,res)))

    def show_postorder(self):
        res = self.tree.postorder()
        self._set_output("Pos Ordem: " + " ".join(map(str,res)))

    def show_textual(self, auto=False):
        txt = self.tree.to_levels_text()
        if auto:
            self._set_output(txt)
        else:
            self._set_output(txt)

    def _set_output(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def draw_tree_window(self):
        win = tk.Toplevel(self.root)
        win.title("Desenho da Árvore")

        fig = plt.Figure(figsize=(6,4))
        ax = fig.add_subplot(111)
        ax.set_axis_off()

        G = self.tree.to_networkx()
        if len(G.nodes) == 0:
            ax.text(0.5,0.5,"<árvore vazia>", horizontalalignment='center', verticalalignment='center')
        else:
            pos = hierarchy_pos(G, self.tree.root.key)
            nx.draw(G, pos=pos, with_labels=True, arrows=False, ax=ax, node_size=800, font_size=10)

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {root:(xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.successors(root))
    if not children:
        return pos
    dx = width/len(children)
    nextx = xcenter - width/2 - dx/2
    for child in children:
        nextx += dx
        pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                            vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root)
    return pos

def main():
    root = tk.Tk()
    app = TreeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
