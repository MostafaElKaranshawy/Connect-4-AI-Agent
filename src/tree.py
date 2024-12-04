from graphviz import Digraph
from node import Node

from node_type import NodeType

class TreeVisualizer:
    def __init__(self, root):
        self.root = root

    def generate_graph(self, node=None, graph=None):
        """Recursively generates the graph."""
        if graph is None:
            graph = Digraph(strict=True)

        if node is None:
            node = self.root
        if node.type == NodeType.MAXIMIZE:
            shape = 'trapezium'
        elif node.type == NodeType.MINIMIZE:
            shape = 'invtrapezium'
        elif node.type == NodeType.CHANCE:
            shape = 'circle'
        else:
            shape = 'triangle'
        # Add the current node to the graph with the specific shape
        label_parts = [
            f"col={node.col}",
            f"val={node.value}"
        ]
        if node.alpha is not None:
            label_parts.append(f"alpha={node.alpha}")
        if node.beta is not None:
            label_parts.append(f"beta={node.beta}")

        label = "\n".join(label_parts)

        graph.node(str(id(node)), label=label, shape=shape)

        # Add edges for children
        for child in node.children:
            graph.edge(str(id(node)), str(id(child)))
            self.generate_graph(child, graph)

        return graph

    def render_tree(self):
        """Generates and renders the tree as an image."""
        graph = self.generate_graph()
        graph.render('tree_output', format='png', cleanup=True)  # Save as PNG

    def display_tree(self):
        """Generates and displays the tree inline in a Jupyter notebook (if applicable)."""
        graph = self.generate_graph()
        return graph.view()  # This will display the tree in the default viewer