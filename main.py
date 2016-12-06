import chess
import time
from timeit import default_timer as timer

white_win_value = float("inf")
black_win_value = float("-inf")
my_globals = {'nodes': 0}

def material(board, color):
    return len(board.pieces(chess.PAWN, color))\
           + (3 * len(board.pieces(chess.KNIGHT, color)))\
           + (3 * len(board.pieces(chess.BISHOP, color)))\
           + (5 * len(board.pieces(chess.ROOK, color)))\
           + (9 * len(board.pieces(chess.QUEEN, color)))


def evaluate(board):
    if board.is_game_over():
        if board.result() == "0-1":
            return black_win_value
        if board.result() == "1-0":
            return white_win_value
        else: return 0
    return material(board, chess.WHITE) - material(board, chess.BLACK)


# white is max agent
def max_value(board, depth):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    v = black_win_value
    for move in board.legal_moves:
        board.push(move)
        my_globals['nodes'] += 1
        v = max(v, min_value(board, depth-1))
        board.pop()
    return v


# black is min agent
def min_value(board, depth):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    v = white_win_value
    for move in board.legal_moves:
        board.push(move)
        my_globals['nodes'] += 1
        v = min(v, max_value(board, depth-1))
        board.pop()
    return v


def search_max(board, depth):
    # white to move - choose highest of next min_values
    best_move = None
    best_value = black_win_value
    for move in board.legal_moves:
        board.push(move)
        my_globals['nodes'] += 1
        v = min_value(board, depth-1)
        board.pop()
        if v > best_value:
            best_value = v
            best_move = move
    return best_move


def search_min(board, depth):
    # white to move - choose lowest of next max_values
    best_move = None
    best_value = white_win_value
    for move in board.legal_moves:
        board.push(move)
        my_globals['nodes'] += 1
        v = max_value(board, depth-1)
        board.pop()
        if v < best_value:
            best_value = v
            best_move = move
    return best_move


def search(board, depth):
    start = timer()
    my_globals['nodes'] = 0
    move = None
    if board.turn:
        # white to move
        move = search_max(board, depth)
    else:
        # black to move
        move = search_min(board, depth)
    end = timer()
    seconds = end - start
    print "time", seconds
    print "kn/s", my_globals['nodes'] / 1000.0 / seconds
    print "move",
    return move


test_board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
print search(test_board, 2)
print ""
print search(test_board, 3)
