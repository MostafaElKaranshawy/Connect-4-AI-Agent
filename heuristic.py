
# Original heuristic function


# def _compute_score(self, board, player):
#     score = 0
#
#     # Right
#     visited = set()
#     for i in range(self.rows):
#         for j in range(self.cols - 3):
#             if (i, j) in visited:
#                 break
#
#             if board[i][j] == player:
#                 length = self._count_sequence(i, j, 0, 1, board, player)
#                 if length >= 4:
#                     score += (length - 3)
#                     for k in range(length):  # Mark cells in this sequence as visited
#                         visited.add((i, j + k))
#
#     # Down
#     visited.clear()
#     for i in range(self.rows - 3):  # Only iterate where 4 rows are available
#         for j in range(self.cols):
#             if (i, j) not in visited and board[i][j] == player:
#                 length = self._count_sequence(i, j, 1, 0, board, player)
#                 if length >= 4:
#                     score += (length - 3)
#                     for k in range(length):  # Mark cells in this sequence as visited
#                         visited.add((i + k, j))
#
#     # Diagonal Down-Right
#     visited.clear()
#     for i in range(self.rows - 3):
#         for j in range(self.cols - 3):
#             if (i, j) not in visited and board[i][j] == player:
#                 length = self._count_sequence(i, j, 1, 1, board, player)
#                 if length >= 4:
#                     score += (length - 3)
#                     for k in range(length):  # Mark cells in this sequence as visited
#                         visited.add((i + k, j + k))
#
#     # Diagonal Down-Left
#     visited.clear()
#     for i in range(self.rows - 3):
#         for j in range(3, self.cols):
#             if (i, j) not in visited and board[i][j] == player:
#                 length = self._count_sequence(i, j, 1, -1, board, player)
#                 if length >= 4:
#                     score += (length - 3)
#                     for k in range(length):  # Mark cells in this sequence as visited
#                         visited.add((i + k, j - k))
#
#     return score
#
