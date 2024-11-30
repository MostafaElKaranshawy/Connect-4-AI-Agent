import math

from node import Node

class MinMaxPrune:
    def __init__(self, computer, human, k):
        self.computer = computer
        self.human = human
        self.max_depth = k
        self.rows = 6
        self.cols = 7


    def decide_ai_move(self, board):
        root = Node()
        depth = self.max_depth
        alpha = -math.inf
        beta = math.inf

        optimal_col, _ = self._maximize(board, root, depth, alpha, beta)
        # root.print_tree()
        return optimal_col, root


    # Maximize function
    def _maximize(self, board, root, depth, alpha, beta):
        if self._is_terminal(board) or depth == 0:
            heuristic_value = self._evaluate(board)
            root.value = heuristic_value
            return None, heuristic_value

        max_col = None
        max_utility = -math.inf

        i = 0
        children, columns = self._get_children(board, self.computer)
        for child in children:
            col = columns[i]

            child_node = Node(col = col)
            root.add_child(child_node)

            _, utility = self._minimize(child, child_node, depth - 1, alpha, beta)
            if utility > max_utility:
                max_col = col
                max_utility = utility

            alpha = max(alpha, max_utility)  # Update alpha
            if beta <= alpha:  # Prune the branch
                break

            i += 1

        root.value = max_utility
        return max_col, max_utility

    def _minimize(self, board, root, depth, alpha, beta):
        if self._is_terminal(board) or depth == 0:
            heuristic_value = self._evaluate(board)
            root.value = heuristic_value
            return None, heuristic_value

        min_col = None
        min_utility = math.inf

        i = 0
        children, columns = self._get_children(board, self.human)
        for child in children:
            col = columns[i]

            child_node = Node(col = col)
            root.add_child(child_node)

            _, utility = self._maximize(child, child_node, depth - 1, alpha, beta)
            if utility < min_utility:
                min_col = col
                min_utility = utility

            beta = min(beta, min_utility)  # Update beta
            if beta <= alpha:  # Prune the branch
                break

            i += 1

        root.value = min_utility
        return min_col, min_utility


    def _count_sequence(self, i, j, di, dj, board, player):
        count = 0
        while 0 <= i < self.rows and 0 <= j < self.cols and board[i][j] == player:
            count += 1
            i, j = i + di, j + dj
        return count


    def _compute_score(self, board, player):
        score = 0

        # Right
        visited = set()
        for i in range(self.rows):
            for j in range(self.cols - 3):
                if (i, j) in visited:
                    break

                if board[i][j] == player:
                    length = self._count_sequence(i, j, 0, 1, board, player)
                    if length >= 4:
                        score += (length - 3)
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i, j + k))

        # Down
        visited.clear()
        for i in range(self.rows - 3):  # Only iterate where 4 rows are available
            for j in range(self.cols):
                if (i, j) not in visited and board[i][j] == player:
                    length = self._count_sequence(i, j, 1, 0, board, player)
                    if length >= 4:
                        score += (length - 3)
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i + k, j))

        # Diagonal Down-Right
        visited.clear()
        for i in range(self.rows - 3):
            for j in range(self.cols - 3):
                if (i, j) not in visited and board[i][j] == player:
                    length = self._count_sequence(i, j, 1, 1, board, player)
                    if length >= 4:
                        score += (length - 3)
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i + k, j + k))

        # Diagonal Down-Left
        visited.clear()
        for i in range(self.rows - 3):
            for j in range(3, self.cols):
                if (i, j) not in visited and board[i][j] == player:
                    length = self._count_sequence(i, j, 1, -1, board, player)
                    if length >= 4:
                        score += (length - 3)
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i + k, j - k))

        return score

    def _evaluate(self, board):

        #calculate the heuristic score
        return self._compute_score(board, self.computer) - self._compute_score(board, self.human)

    # Check if the game is terminal
    def _is_terminal(self, board):
        return all(board[0][col] != 0 for col in range(self.cols))

    def _get_children(self, board, player):
        children = []
        columns = []
        for col in range(self.cols):
            if board[0][col] == 0:
                columns.append(col)

                new_board = [row[:] for row in board]

                # Drop the piece into the lowest available row in the column
                for row in range(self.rows - 1, -1, -1):
                    if new_board[row][col] == 0:
                        new_board[row][col] = player
                        break
                children.append(new_board)
        return children, columns



# min_max_prune = MinMaxPrune(1, 2, 10)
# board = [[0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0],
#          [0, 1, 0, 1, 0, 0, 0],
#          [2, 2, 1, 1, 0, 0, 0],
#          [2, 2, 2, 1, 0, 0, 0]]
#
# print(min_max_prune.decide_ai_move(board))