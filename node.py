class Node:

    def __init__(self, value = None, col = None):
        self.col = col
        self.value = value  # Data held by the node
        self.children = []  # List to store child nodes

    def add_child(self, child_node):
        self.children.append(child_node)

    def print_tree(self, level=0):
        print(" " * (level * 2) + f"(col={self.col}, val={self.value})")
        for child in self.children:
            child.print_tree(level + 1)