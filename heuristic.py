
# leave this file for now


#
#
#
# def compute_score(board, player):
#     """
#     Compute the score of a given player in a modified Connect 4 game.
#
#     :param board: 2D list representing the game board.
#     :param player: Player identifier (e.g., 1 or 2).
#     :return: Score of the player.
#     """
#     rows, cols = len(board), len(board[0])
#     score = 0
#
#     def count_sequence(r, c, dr, dc):
#         count = 0
#         while 0 <= r < rows and 0 <= c < cols and board[r][c] == player:
#             count += 1
#             r, c = r + dr, c + dc
#         return count
#
#     # Right
#     visited = set()
#     for r in range(rows):
#         for c in range(cols - 3):
#             if (r, c) in visited:
#                 break
#
#             if board[r][c] == player:
#                 length = count_sequence(r, c, 0, 1)
#                 if length >= 4:
#                     score += (length - 3)
#                     for i in range(length):  # Mark cells in this sequence as visited
#                         visited.add((r, c + i))
#
#     # Down
#     visited_down = set()
#     for r in range(rows - 3):  # Only iterate where 4 rows are available
#         for c in range(cols):
#             if (r, c) not in visited_down and board[r][c] == player:
#                 length = count_sequence(r, c, 1, 0)
#                 if length >= 4:
#                     score += (length - 3)
#                     for i in range(length):  # Mark cells in this sequence as visited
#                         visited_down.add((r + i, c))
#
#     # Diagonal Down-Right
#     visited.clear()
#     for r in range(rows - 3):
#         for c in range(cols - 3):
#             if (r, c) not in visited and board[r][c] == player:
#                 length = count_sequence(r, c, 1, 1)
#                 if length >= 4:
#                     score += (length - 3)
#                     for i in range(length):  # Mark cells in this sequence as visited
#                         visited.add((r + i, c + i))
#
#     # Diagonal Down-Left
#     visited.clear()
#     for r in range(rows - 3):
#         for c in range(3, cols):
#             if (r, c) not in visited and board[r][c] == player:
#                 length = count_sequence(r, c, 1, -1)
#                 if length >= 4:
#                     score += (length - 3)
#                     for i in range(length):  # Mark cells in this sequence as visited
#                         visited.add((r + i, c - i))
#
#     return score
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
