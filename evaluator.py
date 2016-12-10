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

def material_score(board, color):
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

    return material_score(board, chess.WHITE) - material_score(board, chess.BLACK)
    # material_score = (material(board, chess.WHITE) - material(board, chess.BLACK)) / 39.0
    # position_score = (table_eval(board, chess.WHITE) - table_eval(board, chess.BLACK)) / num_pieces(board)
    #
    # mat_weight = 10.0
    # pos_weight = 4.0
    #
    # return (mat_weight * material_score) + (pos_weight * position_score)

def num_controlled_squares(board):
    controlled_squares = 0
    for _ in chess.SQUARES:
        if len(board.attackers(chess.WHITE, chess.F3)) > len(board.attackers(chess.BLACK, chess.F3)):
            controlled_squares += 1
    return controlled_squares

def naive_mob_score(board):
    return len(list(board.legal_moves))

# finds controlled square advantage
def mob_eval(board, color):
    return num_controlled_squares(board)
    # return mob_score = naive_mob_score(board)

def ps_eval(board, color):
    score = 0
    w_pawns = board.pieces(chess.PAWN, color)
    b_pawns = board.pieces(chess.PAWN, color)
    pawn_columns = {}

    num_doubled_pawns = 0
    num_pawn_rams = 0
    num_isolated_pawns = 0
    num_passed_pawns = 0

    pawn_ram_weight = 1.0
    doubled_pawn_weight = 1.0
    isolated_pawn_weight = 1.0
    passed_pawn_weight = 1.0
    eight_pawn_penalty = 0.2


    for pawn in w_pawns:

        # check for passed pawns
        passed = True
        for b_p in b_pawns:
            if (pawn % 7) == (b_p % 7) and b_p < pawn:
                passed = False
        if passed:
            num_passed_pawns += 1
        # pawn rams
        if (pawn - 8) in b_pawns:
                num_pawn_rams += 1
        # isolated pawns
        if (pawn - 1) % 7 not in pawn_columns and (pawn + 1) % 7 not in pawn_columns:
            num_isolated_pawns += 1
        # doubled pawns
        if (pawn % 7) in pawn_columns:
            num_doubled_pawns += 1
        else:
            pawn_columns[(pawn % 7)] = 1

    if (len(w_pawns) > 7):
        score -= eight_pawn_penalty
    score -= num_doubled_pawns * doubled_pawn_weight
    score -= num_pawn_rams * pawn_ram_weight
    score -= num_isolated_pawns * isolated_pawn_weight
    score += num_passed_pawns * passed_pawn_weight

    return score

class Evaluator():
    def __init__(self, board=None):
        self._pos_dict = {}

    # set major_piece = -1 for total piece count
    def num_major_pieces(self, board):
        pieces = 0
        for square in chess.SQUARES:
            if board.piece_at(square) and not chess.PAWN:
                pieces += 1
        return pieces

    # def num_major_pieces(self, board):
    #     major_pieces = 0
    #     for square in chess.SQUARES:
    #         if board.piece_at(square) and board.piece_at(square) is not chess.PAWN:
    #             major_pieces += 1
    #     return major_pieces

    def openinggame_eval(self, board):
        score = 0

        mat_score = material_score(board, chess.WHITE) - material_score(board, chess.BLACK)
        pos_score = table_eval(board, chess.WHITE) - table_eval(board, chess.BLACK)
        mob_score = mob_eval(board, chess.WHITE)
        ps_score = ps_eval(board, chess.WHITE)

        feature_scores = [mat_score, pos_score, mob_score, ps_score]
        normalized_scores = [float(i)/sum(feature_scores) for i in feature_scores]
        feature_weights = [1.0, 1.0, 1.0, 1.0]

        for i in range(len(feature_scores)):
            score += normalized_scores[i] * feature_weights[i]

        return score

    def middlegame_eval(self, board):
        score = 0

        mat_score = material_score(board, chess.WHITE) - material_score(board, chess.BLACK)
        pos_score = table_eval(board, chess.WHITE) - table_eval(board, chess.BLACK)
        mob_score = mob_eval(board, chess.WHITE)
        ps_score = ps_eval(board, chess.WHITE)

        feature_scores = [mat_score, pos_score, mob_score, ps_score]
        normalized_scores = [float(i)/sum(feature_scores) for i in feature_scores]
        feature_weights = [1.0, 1.0, 1.0, 1.0]

        # include too

        for i in range(len(feature_scores)):
            score += normalized_scores[i] * feature_weights[i]

        return score

    def endgame_eval(self, board):
        score = 0

        mat_score = material_score(board, chess.WHITE) - material_score(board, chess.BLACK)
        pos_score = table_eval(board, chess.WHITE) - table_eval(board, chess.BLACK)
        mob_score = mob_eval(board, chess.WHITE)
        ps_score = ps_eval(board, chess.WHITE)

        feature_scores = [mat_score, pos_score, mob_score, ps_score]
        normalized_scores = [float(i)/sum(feature_scores) for i in feature_scores]
        feature_weights = [1.0, 1.0, 1.0, 1.0]

        # includes king safety
        # include pawn advantage

        for i in range(len(feature_scores)):
            score += normalized_scores[i] * feature_weights[i]

        return score

    # returns evaluation score for white
    def evaluate(self, board):
        if board.zobrist_hash() in self._pos_dict:
            return self._pos_dict.get(board.zobrist_hash)

        if self.num_major_pieces(board) > 12:
            score = self.openinggame_eval(board)
        elif self.num_major_pieces(board) > 7:
            score = self.middlegame_eval(board)
        else:
            score = self.endgame_eval(board)

        self._pos_dict[board.zobrist_hash] = score
        return score


if __name__ == '__main__':
    raise NotImplemented
