from graphviz import Digraph

class TreeVisualizer:
    def __init__(self, root):
        self.root = root

    def generate_graph(self, node=None, graph=None):
        """Recursively generates the graph."""
        if graph is None:
            graph = Digraph(strict=True)

        if node is None:
            node = self.root

        # Determine the shape based on the node type
        if node.type == "MAXIMIZE":
            shape = "trapezium"  # Upper trapezoid
        elif node.type == "MINIMIZE":
            shape = "invtrapezium"  # Downward trapezoid
        elif node.type == "CHANCE":
            shape = "circle"  # Circle
        else:
            shape = "box"  # Default shape

        # Add the current node to the graph with the specific shape
        graph.node(str(id(node)), label=f"col={node.col}\nval={node.value}", shape=shape)

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