import math
from node import Node


class ExpectedMinMax:
    def __init__(self, computer, human, k):
        self.computer = computer
        self.human = human
        self.max_depth = k
        self.rows = 6
        self.cols = 7
        self.memo = {}  # Dictionary to store memoized results

    def decide_ai_move(self, board):
        root = Node(type="max")
        depth = self.max_depth
        optimal_col, _ = self._maximize(board, root, depth)
        root.col = optimal_col
        self.memo.clear()
        print("done")
        return optimal_col, root


    def _maximize(self, board, root, depth):
        board_key = self._hash_board(board)
        if (board_key) in self.memo:
            root.value = self.memo[(board_key)]
            return None, root.value

        if self._is_terminal(board) or depth == 0:
            heuristic_value = self._evaluate(board)
            root.value = heuristic_value
            self.memo[(board_key)] = heuristic_value
            return None, heuristic_value

        max_col = None
        max_utility = -math.inf

        children, columns = self._get_children(board, self.computer)
        for i, child in enumerate(children):
            col = columns[i]

            chance_node = Node(col=col, type="chance")
            root.add_child(chance_node)

            utility = self.calculate_utility(board, col, child, chance_node, depth, self.computer)
            if utility > max_utility:
                max_col = col
                max_utility = utility

        root.value = max_utility
        self.memo[(board_key)] = max_utility
        return max_col, max_utility

    def _minimize(self, board, root, depth):
        board_key = self._hash_board(board)
        if (board_key) in self.memo:
            root.value = self.memo[(board_key)]
            return None, root.value

        if self._is_terminal(board) or depth == 0:
            heuristic_value = self._evaluate(board)
            root.value = heuristic_value
            self.memo[(board_key)] = heuristic_value
            return None, heuristic_value

        min_col = None
        min_utility = math.inf

        children, columns = self._get_children(board, self.human)
        for i, child in enumerate(children):
            col = columns[i]

            chance_node = Node(col=col, type="chance")
            root.add_child(chance_node)

            utility = self.calculate_utility(board, col, child, chance_node, depth, self.human)
            if utility < min_utility:
                min_col = col
                min_utility = utility

        root.value = min_utility
        self.memo[(board_key)] = min_utility
        return min_col, min_utility

    def calculate_utility(self, board, col, child, chance_node, depth, player):
        utility = 0

        # 20% probability of the left column (if valid)
        if col > 0:
            left_child = self._get_child_with_column(board, col - 1, player)
            if left_child:
                left_child_node = Node(col=col - 1, type="max" if player == self.computer else "min")
                chance_node.add_child(left_child_node)
                _, left_utility = self._minimize(left_child, left_child_node, depth - 1) \
                    if player == self.computer else self._maximize(left_child, left_child_node, depth - 1)
                utility += 0.2 * left_utility
                left_child_node.value = left_utility

        # 60% probability of the chosen column
        child_node = Node(col=col)
        chance_node.add_child(child_node)
        _, chosen_utility = self._minimize(child, child_node, depth - 1) \
            if player == self.computer else self._maximize(child, child_node, depth - 1)

        utility += 0.6 * chosen_utility
        child_node.value = chosen_utility

        # 20% probability of the right column (if valid)
        if col < self.cols - 1:
            right_child = self._get_child_with_column(board, col + 1, player)
            if right_child:
                right_child_node = Node(col=col + 1)
                chance_node.add_child(right_child_node)
                _, right_utility = self._minimize(right_child, right_child_node, depth - 1) \
                    if player == self.computer else self._maximize(right_child, right_child_node, depth - 1)
                utility += 0.2 * right_utility
                right_child_node.value = right_utility

        return utility

    def _count_sequence(self, i, j, di, dj, board, player):
        count = 0
        while 0 <= i < self.rows and 0 <= j < self.cols and board[i][j] == player:
            count += 1
            i, j = i + di, j + dj
        return count

    def _compute_score(self, board, player):
        score = 0

        # Right
        for i in range(self.rows):
            for j in range(self.cols - 3):
                if board[i][j] == player:
                    score += self._count_sequence(i, j, 0, 1, board, player) >= 4

        # Down
        for i in range(self.rows - 3):
            for j in range(self.cols):
                if board[i][j] == player:
                    score += self._count_sequence(i, j, 1, 0, board, player) >= 4

        # Diagonal Down-Right
        for i in range(self.rows - 3):
            for j in range(self.cols - 3):
                if board[i][j] == player:
                    score += self._count_sequence(i, j, 1, 1, board, player) >= 4

        # Diagonal Down-Left
        for i in range(self.rows - 3):
            for j in range(3, self.cols):
                if board[i][j] == player:
                    score += self._count_sequence(i, j, 1, -1, board, player) >= 4

        return score

    def _evaluate(self, board):
        return self._compute_score(board, self.computer) - self._compute_score(board, self.human)

    def _is_terminal(self, board):
        return all(board[0][col] != 0 for col in range(self.cols))

    def _get_children(self, board, player):
        children = []
        columns = []
        for col in range(self.cols):
            if board[0][col] == 0:
                new_board = [row[:] for row in board]
                for row in range(self.rows - 1, -1, -1):
                    if new_board[row][col] == 0:
                        new_board[row][col] = player
                        break
                children.append(new_board)
                columns.append(col)
        return children, columns

    def _get_child_with_column(self, board, col, player):
        if board[0][col] != 0:
            return None
        new_board = [row[:] for row in board]
        for row in range(self.rows - 1, -1, -1):
            if new_board[row][col] == 0:
                new_board[row][col] = player
                break
        return new_board

    def _hash_board(self, board):
        return tuple(tuple(row) for row in board)
