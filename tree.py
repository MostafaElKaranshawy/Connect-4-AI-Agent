import pygame
from pygame import FULLSCREEN
from node import Node  # Import the Node class

class Tree:
    def __init__(self, root):
        # Step 1: Calculate the total size of the tree
        positions = {}
        self.calculate_positions(root, 400, 100, 100, 100, positions)

        pygame.init()
        self.screen_width = 2000  # Set to your desired screen width
        self.screen_height = 1000  # Set to your desired screen height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tree Visualization")
        clock = pygame.time.Clock()

        # Step 2: Calculate tree dimensions
        min_x, max_x, min_y, max_y = self.calculate_tree_bounds(positions)

        # Step 3: Calculate scaling factor to fit tree within screen size
        scale_factor = min(self.screen_width / (max_x - min_x), self.screen_height / (max_y - min_y))

        # Step 4: Rescale positions
        self.rescale_positions(positions, scale_factor, min_x, min_y)

        # Draw the tree
        screen = pygame.display.set_mode((2000, 1000))
        screen.fill((255, 255, 255))
        self.draw_tree(self.screen, root, positions)
        pygame.display.flip()
        clock.tick(60)

        # pygame.quit()

    def calculate_positions(self, node, x, y, x_spacing, y_spacing, positions):
        """Recursively calculate positions for each node."""
        positions[node] = (x, y)
        if not node.children:
            return

        # Calculate child positions
        child_count = len(node.children)
        start_x = x - (child_count - 1) * x_spacing // 2
        for i, child in enumerate(node.children):
            self.calculate_positions(
                child,
                start_x + i * x_spacing,
                y + y_spacing,
                x_spacing,
                y_spacing,
                positions
            )

    def calculate_tree_bounds(self, positions):
        """Calculate the minimum and maximum x and y coordinates of the tree."""
        min_x = min(positions[node][0] for node in positions)
        max_x = max(positions[node][0] for node in positions)
        min_y = min(positions[node][1] for node in positions)
        max_y = max(positions[node][1] for node in positions)
        return min_x, max_x, min_y, max_y

    def rescale_positions(self, positions, scale_factor, min_x, min_y):
        """Rescale the positions based on the scale factor."""
        for node in positions:
            x, y = positions[node]
            # Apply scaling
            new_x = (x - min_x) * scale_factor
            new_y = (y - min_y) * scale_factor
            positions[node] = (new_x, new_y)

    def draw_tree(self, screen, node, positions):
        """Recursively draw nodes and edges."""
        if node not in positions:
            return

        # Draw edges to children
        for child in node.children:
            if child in positions:
                pygame.draw.line(screen, (0, 0, 0), positions[node], positions[child], 2)

        # Draw the node (scale size based on the screen)
        pygame.draw.circle(screen, (0, 100, 200), positions[node], 20)
        font = pygame.font.Font(None, 24)
        text = font.render(str(node.value), True, (255, 255, 255))
        text_rect = text.get_rect(center=positions[node])
        screen.blit(text, text_rect)

        # Recursively draw children
        for child in node.children:
            self.draw_tree(screen, child, positions)


# Example usage:
if __name__ == "__main__":
    # Create a sample tree structure
    root = Node(value="A", col=1)
    b = Node(value="B", col=2)
    c = Node(value="C", col=3)
    d = Node(value="D", col=4)
    e = Node(value="E", col=5)
    f = Node(value="F", col=6)

    root.add_child(b)
    root.add_child(c)
    b.add_child(d)
    b.add_child(e)
    c.add_child(f)

    # Create and run the tree visualization
    Tree(root)
