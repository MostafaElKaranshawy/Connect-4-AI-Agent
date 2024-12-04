
from min_max_prune import MinMaxPrune

def bonus_function(board, turn):
    min_max_prune = MinMaxPrune(turn, 3 - turn, 8)

    return min_max_prune.decide_ai_move(board)