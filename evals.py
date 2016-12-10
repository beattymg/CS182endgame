import chess
import chess.polyglot
from timeit import default_timer as timer
import random

white_win_value = float("inf")
black_win_value = float("-inf")

pawn_table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              50, 50, 50, 50, 50, 50, 50, 50,
              10, 10, 20, 30, 30, 20, 10, 10,
              5,  5, 10, 25, 25, 10,  5,  5,
              0,  0,  0, 20, 20,  0,  0,  0,
              5, -5,-10,  0,  0,-10, -5,  5,
              5, 10, 10,-20,-20, 10, 10,  5,
              0,  0,  0,  0,  0,  0,  0,  0]

knight_table = [-50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50]

bishop_table = [-20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20]

rook_table = [0,  0,  0,  0,  0,  0,  0,  0,
              5, 10, 10, 10, 10, 10, 10,  5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
              0,  0,  0,  5,  5,  0,  0,  0]

queen_table = [-20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20]

king_table = [-30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20]

# create 64 length lists -- ie tables for each piece
# go through table:

def table_eval(board, color):
    score = 0

    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    for piece in piece_types:
        piece_squares = board.pieces(piece, color)
        for square in piece_squares:
            if color is chess.BLACK:
                square = flip(square)

            if piece is chess.PAWN:
                score += (pawn_table[square] / 50.0)
            elif piece is chess.KNIGHT:
                score += (knight_table[square] / 50.0)
            elif piece is chess.BISHOP:
                score += (bishop_table[square] / 50.0)
            elif piece is chess.ROOK:
                score += (rook_table[square] / 50.0)
            elif piece is chess.QUEEN:
                score += (queen_table[square] / 50.0)
            elif piece is chess.KING:
                score += (king_table[square] / 50.0)

    return score


def flip(square):
    return (7 - (square % 8)) + ((7 - (square // 8)) * 8)

def num_pieces(board):
    pieces = 0
    for s in chess.SQUARES:
        if board.piece_at(s):
            pieces += 1
    return pieces

def material(board, color):
    return len(board.pieces(chess.PAWN, color))\
           + (3.0 * len(board.pieces(chess.KNIGHT, color)))\
           + (3.0 * len(board.pieces(chess.BISHOP, color)))\
           + (5.0 * len(board.pieces(chess.ROOK, color)))\
           + (9.0 * len(board.pieces(chess.QUEEN, color)))


def evaluate(board):
    if board.is_game_over():
        if board.result() == "0-1":
            return black_win_value
        if board.result() == "1-0":
            return white_win_value
        else: return 0

    return material(board, chess.WHITE) - material(board, chess.BLACK)
    # material_score = (material(board, chess.WHITE) - material(board, chess.BLACK)) / 39.0
    # position_score = (table_eval(board, chess.WHITE) - table_eval(board, chess.BLACK)) / num_pieces(board)
    #
    # mat_weight = 10.0
    # pos_weight = 4.0
    #
    # return (mat_weight * material_score) + (pos_weight * position_score)

if __name__ == '__main__':
    raise NotImplemented
