# Importa 'deque' da biblioteca 'collections', que usaremos para uma fila eficiente.
from collections import deque

class Node:
    """
    Classe que representa um único nó na árvore binária.
    """
    def __init__(self, data):
        self.data = data  # O valor que o nó armazena
        self.left = None  # O filho da esquerda (inicialmente vazio)
        self.right = None # O filho da direita (inicialmente vazio)

    def __str__(self):
        # Isso ajuda a printar o valor do nó de forma amigável
        return str(self.data)

class BinaryTree:
    """
    Classe que representa a Árvore Binária e suas operações.
    """
    def __init__(self):
        self.root = None # A raiz da árvore (inicialmente vazia)

    # --- MÉTODOS A SEREM IMPLEMENTADOS ---
    
    # Etapa 1: Inserção
    
    def insert_level_order(self, data):
        """
        Insere um novo nó na árvore no primeiro espaço disponível,
        usando a ordem por nível (level-order).
        """
        new_node = Node(data)
        
        # Caso 1: A árvore está vazia. O novo nó é a raiz.
        if self.root is None:
            self.root = new_node
            return

        # Caso 2: A árvore não está vazia. Usamos uma fila para achar o lugar.
        queue = deque([self.root]) # Cria a fila e já adiciona a raiz

        while queue:
            current_node = queue.popleft() # Pega o primeiro da fila

            # Verifica o filho da esquerda
            if current_node.left is None:
                current_node.left = new_node
                return # Inseriu, pode parar
            else:
                queue.append(current_node.left) # Adiciona no fim da fila

            # Verifica o filho da direita
            if current_node.right is None:
                current_node.right = new_node
                return # Inseriu, pode parar
            else:
                queue.append(current_node.right) # Adiciona no fim da fila

    # Etapa 2: Travessias

    # --- IN-ORDER ---
    def get_inorder(self):
        """Retorna uma lista com os valores da travessia in-order."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, current_node, result):
        if current_node: # Se o nó não for None
            self._inorder(current_node.left, result)
            result.append(current_node.data)
            self._inorder(current_node.right, result)

    # --- PRE-ORDER ---
    def get_preorder(self):
        """Retorna uma lista com os valores da travessia pre-order."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, current_node, result):
        if current_node:
            result.append(current_node.data)
            self._preorder(current_node.left, result)
            self._preorder(current_node.right, result)

    # --- POST-ORDER ---
    def get_postorder(self):
        """Retorna uma lista com os valores da travessia post-order."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, current_node, result):
        if current_node:
            self._postorder(current_node.left, result)
            self._postorder(current_node.right, result)
            result.append(current_node.data)

    # --- LEVEL-ORDER ---
    def get_level_order(self):
        """Retorna uma lista com os valores da travessia por nível."""
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

    # Etapa 3: Classificações

    # --- FUNÇÕES AUXILIARES ---
    def _get_height(self, node):
        """Função auxiliar para calcular a altura de uma sub-árvore."""
        if node is None:
            return -1 # Altura de uma árvore vazia
        
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        
        return 1 + max(left_height, right_height)

    def _is_regular_recursive(self, node):
        """Função auxiliar para checar se a árvore é regular."""
        if node is None:
            return True # Sub-árvore vazia é considerada regular
        
        # Se um nó tem um filho mas não o outro
        if (node.left is None and node.right is not None) or \
           (node.left is not None and node.right is None):
            return False
            
        # Checa recursivamente para os filhos
        return self._is_regular_recursive(node.left) and self._is_regular_recursive(node.right)

    def _is_balanced_recursive(self, node):
        """
        Função auxiliar que checa o balanceamento e retorna um par:
        (is_balanced, height)
        """
        if node is None:
            return (True, -1)

        is_left_balanced, left_height = self._is_balanced_recursive(node.left)
        if not is_left_balanced:
            return (False, 0)

        is_right_balanced, right_height = self._is_balanced_recursive(node.right)
        if not is_right_balanced:
            return (False, 0)
        
        balanced = abs(left_height - right_height) <= 1
        height = 1 + max(left_height, right_height)
        
        return (balanced, height)

    # --- MÉTODOS DE CLASSIFICAÇÃO ---
    def is_regular(self):
        """Verifica se a árvore é regular (cada nó tem 0 ou 2 filhos)."""
        return self._is_regular_recursive(self.root)

    def is_perfect(self):
        """Verifica se a árvore é perfeita."""
        height = self._get_height(self.root)
        node_count = len(self.get_level_order()) # Reutilizamos a travessia para contar os nós
        
        # Fórmula matemática para uma árvore perfeita
        return node_count == (2**(height + 1) - 1)

    def is_complete(self):
        """
        Verifica se a árvore é completa.
        (Nossa inserção sempre cria uma árvore completa, então isso deve ser sempre True).
        """
        if self.root is None:
            return True
        
        queue = deque([self.root])
        found_first_gap = False
        
        while queue:
            node = queue.popleft()
            
            if node is None:
                found_first_gap = True
            else:
                if found_first_gap:
                    return False # Encontrou um nó depois de uma falha
                queue.append(node.left)
                queue.append(node.right)
        
        return True

    def is_balanced(self):
        """Verifica se a árvore é balanceada."""
        is_b, _ = self._is_balanced_recursive(self.root)
        return is_b
        
    def is_unbalanced(self):
        """Verifica se a árvore é desbalanceada."""
        return not self.is_balanced()

# --- FIM DAS CLASSES ---

# Área para testar nosso código
if __name__ == "__main__":
    # (O código anterior de criação e travessia permanece o mesmo)
    arvore = BinaryTree()
    valores = [1, 2, 3, 4, 5, 6]
    for valor in valores:
        arvore.insert_level_order(valor)

    print("--- Exemplo de Saída Esperada ---")
    print("Após a inserção dos valores [1, 2, 3, 4, 5, 6]:\n")

    in_order_result = arvore.get_inorder()
    print(f"In-Order: {' '.join(map(str, in_order_result))}")
    pre_order_result = arvore.get_preorder()
    print(f"Pré-Ordem: {' '.join(map(str, pre_order_result))}")
    post_order_result = arvore.get_postorder()
    print(f"Pós-Ordem: {' '.join(map(str, post_order_result))}")
    level_order_result = arvore.get_level_order()
    print(f"Level-Order: {' '.join(map(str, level_order_result))}")
    
    # --- NOVA PARTE DO TESTE ---
    print("\nClassificação da árvore:")
    if arvore.is_complete(): print(" • Completa")
    if arvore.is_perfect(): print(" • Perfeita")
    if arvore.is_regular(): print(" • Regular")
    if arvore.is_balanced(): print(" • Balanceada")
    if arvore.is_unbalanced(): print(" • Desbalanceada")