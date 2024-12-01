import threading

from min_max import MinMax
from min_max_prune import MinMaxPrune
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
            pass

    def computer_choice(self, board):
        move, tree_node = self.method.decide_ai_move(board=board)
        return move, tree_node

    def show_tree(self, tree_node):
        tree = TreeVisualizer(tree_node)
        tree.display_tree()

