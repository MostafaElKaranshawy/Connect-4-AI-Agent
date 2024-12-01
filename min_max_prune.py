import math

from node import Node
from node_type import NodeType

class MinMaxPrune:
    def __init__(self, computer, human, k):
        self.computer = computer
        self.human = human
        self.max_depth = k
        self.rows = 6
        self.cols = 7
        self.memo = {}
        self.weights =  [[3, 4,  5,  10,  5, 4, 3],
                         [4, 6,  8,  15,  8, 6, 4],
                         [5, 8, 11,  20, 11, 8, 5],
                         [5, 8, 11,  20, 11, 8, 5],
                         [4, 6,  8,  15,  8, 6, 4],
                         [3, 4,  5,  10,  5, 4, 3]]


    def decide_ai_move(self, board):
        root = Node(node_type = NodeType.MAXIMIZE)
        depth = self.max_depth
        alpha = -math.inf
        beta = math.inf

        optimal_col, _ = self._maximize(board, root, depth, alpha, beta)

        root.col = optimal_col
        self.memo.clear()

        # root.print_tree()
        return optimal_col, root


    # Maximize function
    def _maximize(self, board, root, depth, alpha, beta):
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

            _, utility = self._minimize(child, child_node, depth - 1, alpha, beta)
            if utility > max_utility:
                max_col = col
                max_utility = utility

            alpha = max(alpha, max_utility)  # Update alpha
            if beta <= alpha:  # Prune the branch
                break

            i += 1

        root.value = max_utility
        self.memo[(board_key)] = (root, max_utility)
        return max_col, max_utility

    def _minimize(self, board, root, depth, alpha, beta):
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

            _, utility = self._maximize(child, child_node, depth - 1, alpha, beta)
            if utility < min_utility:
                min_col = col
                min_utility = utility

            beta = min(beta, min_utility)  # Update beta
            if beta <= alpha:  # Prune the branch
                break

            i += 1

        root.value = min_utility
        self.memo[(board_key)] = (root, min_utility)
        return min_col, min_utility


    def _count_potential_sequence(self, i, j, di, dj, board, player):
        length = 0
        potential = 0

        x, y = i - di, j - dj
        if 0 <= x < self.rows and 0 <= y < self.cols and board[x][y] == 0:
            potential += 1


        # Count the length of the sequence
        while 0 <= i < self.rows and 0 <= j < self.cols and board[i][j] == player:
            length += 1
            i += di
            j += dj

        # Count the potential of the sequence ( number of empty cells on both sides )
        if 0 <= i < self.rows and 0 <= j < self.cols and board[i][j] == 0:
            potential += 1

        return length, potential


    def _blocking_moves(self, board, player):
        opponent = 3 - player   # The opponent of the player
        critical_moves = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for j in range(self.cols):
            # Find the lowest available row in this column
            for i in range(self.rows - 1, -1, -1):
                if board[i][j] == 0:
                    for di, dj in directions:
                        # Check if this move blocks an opponent sequence
                        length, _ = self._count_potential_sequence(i, j, di, dj, board, opponent)
                        if length >= 3:
                            critical_moves += 1
                            break  # one blocking move is enough

                    break  # Only the lowest playable cell in this column matters
        return critical_moves

    def _position_weight(self, board, player):
        score = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] == player:
                    score += self.weights[i][j]
        return score

    def _compute_heuristic(self, board, player):
        score = 0

        # Positional weight
        score += self._position_weight(board, player)

        # add current score of the player
        score += self._compute_score_plus_sides(board, player)

        # Blocking moves (put more weight on blocking moves)
        # if self.max_depth % 2 != 0:
        #     # computer can't defend itself
        #     if player == self.computer:
        #         score += self._blocking_moves(board, player) * 5
        #     else:
        #         score -= self._blocking_moves(board, player) * 5
        #
        # else:
        #     # computer can defend itself
        #     if player == self.computer:
        #         score -= self._blocking_moves(board, player) * 5
        #     else:
        #         score += self._blocking_moves(board, player) * 5


        # OR simply (which one is better?)
        score += self._blocking_moves(board, player) * 5
        return score


    def _compute_score_plus_sides(self, board, player):
        score = 0
        # potential_weight = 3
        potential_weight = 5

        # Right
        visited = set()
        for i in range(self.rows):
            for j in range(self.cols - 3):
                if (i, j) in visited:
                    break

                if board[i][j] == player:
                    length, potential = self._count_potential_sequence(i, j, 0, 1, board, player)
                    if length >= 4:
                        score += (length - 3) + potential * potential_weight
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i, j + k))

                    elif length == 3:
                        score += potential * (potential_weight // 2)


        # Down
        visited.clear()
        for i in range(self.rows - 3):  # Only iterate where 4 rows are available
            for j in range(self.cols):
                if (i, j) not in visited and board[i][j] == player:
                    length, potential = self._count_potential_sequence(i, j, 1, 0, board, player)
                    if length >= 4:
                        score += (length - 3) + potential * potential_weight
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i + k, j))

                    elif length == 3:
                        score += potential * (potential_weight // 2)

        # Diagonal Down-Right
        visited.clear()
        for i in range(self.rows - 3):
            for j in range(self.cols - 3):
                if (i, j) not in visited and board[i][j] == player:
                    length, potential = self._count_potential_sequence(i, j, 1, 1, board, player)
                    if length >= 4:
                        score += (length - 3) + potential * potential_weight
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i + k, j + k))

                    elif length == 3:
                        score += potential * (potential_weight // 2)

        # Diagonal Down-Left
        visited.clear()
        for i in range(self.rows - 3):
            for j in range(3, self.cols):
                if (i, j) not in visited and board[i][j] == player:
                    length, potential = self._count_potential_sequence(i, j, 1, -1, board, player)
                    if length >= 4:
                        score += (length - 3) + potential * potential_weight
                        for k in range(length):  # Mark cells in this sequence as visited
                            visited.add((i + k, j - k))

                    elif length == 3:
                        score += potential * (potential_weight // 2)

        return score

    def _evaluate(self, board):

        #calculate the heuristic score
        return self._compute_heuristic(board, self.computer) - self._compute_heuristic(board, self.human)

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