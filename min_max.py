import math


from node import Node
from node_type import NodeType
from heuristic import Heuristic

class MinMax:
    def __init__(self, computer, human, k):
        self.computer = computer
        self.human = human
        self.max_depth = k
        self.rows = 6
        self.cols = 7
        self.memo = {}
        self.heuristic = Heuristic()
        self.weights =  [[3, 4,  5,  10,  5, 4, 3],
                         [4, 6,  8,  15,  8, 6, 4],
                         [5, 8, 11,  20, 11, 8, 5],
                         [5, 8, 11,  20, 11, 8, 5],
                         [4, 6,  8,  15,  8, 6, 4],
                         [3, 4,  5,  10,  5, 4, 3]]

    def decide_ai_move(self, board):
        root = Node(node_type = NodeType.MAXIMIZE)
        depth = self.max_depth
        optimal_col, _ = self._maximize(board, root, depth)
        root.col = optimal_col
        self.memo.clear()

        return optimal_col, root


    # Maximize function
    def _maximize(self, board, root, depth):
        board_key = self._hash_board(board)
        if (board_key) in self.memo:
            child_node, value = self.memo[(board_key)]
            root = child_node
            return None, root.value


        if self._is_terminal(board) or depth == 0:
            heuristic_value = self._evaluate(board)
            root.value = heuristic_value
            self.memo[(board_key)] = (root, heuristic_value)
            return None, heuristic_value

        max_col = None
        max_utility = -math.inf

        i = 0
        children, columns = self._get_children(board, self.computer)
        for child in children:
            col = columns[i]

            child_node = Node(col = col, node_type = NodeType.MINIMIZE)
            root.add_child(child_node)

            _, utility = self._minimize(child, child_node, depth - 1)
            if utility > max_utility:
                max_col = col
                max_utility = utility

            i += 1

        root.value = max_utility
        self.memo[(board_key)] = (root, max_utility)
        return max_col, max_utility

    def _minimize(self, board, root, depth):
        board_key = self._hash_board(board)
        if (board_key) in self.memo:
            child_node, value = self.memo[(board_key)]
            root = child_node
            return None, root.value


        if self._is_terminal(board) or depth == 0:
            heuristic_value = self._evaluate(board)
            root.value = heuristic_value
            self.memo[(board_key)] = (root, heuristic_value)
            return None, heuristic_value

        min_col = None
        min_utility = math.inf

        i = 0
        children, columns = self._get_children(board, self.human)
        for child in children:
            col = columns[i]

            child_node = Node(col = col, node_type = NodeType.MAXIMIZE)
            root.add_child(child_node)

            _, utility = self._maximize(child, child_node, depth - 1)
            if utility < min_utility:
                min_col = col
                min_utility = utility

            i += 1

        root.value = min_utility
        self.memo[(board_key)] = (root, min_utility)
        return min_col, min_utility

    def _evaluate(self, board):
        #calculate the heuristic score
        return self.heuristic.evaluate(board, self.computer) - self.heuristic.evaluate(board, self.human)

    # Check if the game is terminal
    def _is_terminal(self, board):
        return all(board[0][col] != 0 for col in range(self.cols))

    def _get_children(self, board, player):
        children = []
        columns = []
        for col in range(self.cols):
            if board[0][col] == 0:
                new_board = [row[:] for row in board]

                # Drop the piece into the lowest available row in the column
                for row in range(self.rows - 1, -1, -1):
                    if new_board[row][col] == 0:
                        new_board[row][col] = player
                        break
                children.append(new_board)
                columns.append(col)
        return children, columns

    def _hash_board(self, board):
        return tuple(tuple(row) for row in board)