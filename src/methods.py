import threading

from min_max import MinMax
from min_max_prune import MinMaxPrune
from expected_min_max import ExpectedMinMax
from tree import TreeVisualizer

class Methods:
    def __init__(self, method, computer_turn, k):
        self.computer_turn = computer_turn
        self.human_turn = 1 if computer_turn == 2 else 2
        self.k = k
        print(method)
        if method == "Minmax without pruning":
            self.method = MinMax(self.computer_turn, self.human_turn, self.k)
        elif method == "Alpha-beta Minmax":
            self.method = MinMaxPrune(self.computer_turn, self.human_turn, self.k)
        elif method == "Expectiminmax":
            self.method = ExpectedMinMax(self.computer_turn, self.human_turn, self.k)
    def computer_choice(self, board):
        move, tree_node = self.method.decide_ai_move(board=board)
        self.print_tree(tree_node, prefix="", is_last=True)
        return move, tree_node

    def show_tree(self, tree_node):
        tree = TreeVisualizer(tree_node)
        tree.display_tree()

    # def print_tree(self, node, level=0):
    #     indent = " " * (level * 4)  # Indent for visualization
    #     print(f"{indent}Type: {node.type}, Value: {node.value}, Col: {node.col}")
    #     for child in node.children:
    #         self.print_tree(child, level + 1)

    def print_tree(self, node, prefix="", is_last=True):
        # Print the current node
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}Type: {node.type}, Value: {node.value}, Col: {node.col}")

        # Update the prefix for child nodes
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Recursively print each child node
        for i, child in enumerate(node.children):
            self.print_tree(child, new_prefix, i == len(node.children) - 1)
