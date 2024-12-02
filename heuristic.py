
class Heuristic:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.cache = {}
        self.weights =  [[3, 4,  5,  10,  5, 4, 3],
                         [4, 6,  8,  15,  8, 6, 4],
                         [5, 8, 11,  20, 11, 8, 5],
                         [5, 8, 11,  20, 11, 8, 5],
                         [4, 6,  8,  15,  8, 6, 4],
                         [3, 4,  5,  10,  5, 4, 3]]

    def evaluate(self, board, player):
        board_key = self._hash_board(board)
        if (board_key, player) in self.cache:
            return self.cache[(board_key, player)]

        score = 0
        # Positional weight
        score += self._position_weight(board, player)

        # compute the score for the player
        score += self._compute_score(board, player) * 1000

        # possible fours
        score += self.check_connected_sequences(board, player, 4) * 700

        # possible threes
        score += self.check_connected_sequences(board, player, 3) * 100

        # possible twos
        score += self.check_connected_sequences(board, player, 2) * 10

        # Blocking moves
        score += self.blocking_moves(board, player) * 500

        self.cache[(board_key, player)] = score
        return score

    def _count_sequence(self, i, j, di, dj, board, player):
        length = 0
        # Count the length of the sequence
        while 0 <= i < self.rows and 0 <= j < self.cols and board[i][j] == player:
            length += 1
            i, j = i + di, j + dj

        return length

    def blocking_moves(self, board, player):
        opponent = 3 - player  # The opponent of the player
        critical_moves = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for j in range(self.cols):
            # Find the lowest available row in this column
            for i in range(self.rows - 1, -1, -1):
                if board[i][j] == 0:
                    for di, dj in directions:
                        # Check if this move blocks an opponent sequence
                        length = self._count_sequence(i, j, di, dj, board, opponent)
                        if length >= 3:
                            critical_moves += 1
                            break  # one blocking move is enough

                    break  # Only the lowest playable cell in this column matters
        return critical_moves

    def _position_weight(self, board, player):
        score = 0
        for j in range(self.cols):
            for i in range(self.rows - 1, -1, -1):
                if board[i][j] == player:
                    score += self.weights[i][j]
                elif board[i][j] == 0:
                    break
        return score

    def check_connected_sequences(self, board, player, sequence_to_check):
        opponent = 3 - player

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        connected_sequences = 0

        for i in range(self.rows):
            for j in range(self.cols):

                if board[i][j] == player:
                    for di, dj in directions:
                        count = 1
                        new_i, new_j = i, j
                        empty_before = False
                        empty_within = False

                        if (0 <= new_i - di < self.rows and 0 <= new_j - dj < self.cols
                                and board[new_i - di][new_j - dj] == 0
                                and 0 <= new_i + di + 1 < self.rows and board[new_i - di + 1][new_j - dj] != 0):
                            count += 1
                            empty_before = True

                        for k in range(1, sequence_to_check):
                            new_i, new_j = new_i + di, new_j + dj
                            if not (0 <= new_i < self.rows and 0 <= new_j < self.cols):
                                break

                            if 0 <= new_i + 1 < self.rows and 0 <= new_j < self.cols and board[new_i + 1][
                                new_j] == 0:
                                break

                            if board[new_i][new_j] == opponent:
                                count = 0
                                break

                            if board[new_i][new_j] == player:
                                count += 1

                            elif not empty_within and board[new_i][new_j] == 0:
                                empty_within = True
                                count += 1

                        if count >= sequence_to_check and (empty_within or empty_before):
                            connected_sequences += 1

        return connected_sequences


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
    def _hash_board(self, board):
        return tuple(tuple(row) for row in board)
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
