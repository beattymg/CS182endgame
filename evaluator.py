import chess
import chess.polyglot
import chess.syzygy
from timeit import default_timer as timer
import random

white_win_value = float("inf")
black_win_value = float("-inf")

pawn_table = [198, 198, 198, 198, 198, 198, 198, 198,
              178, 198, 198, 198, 198, 198, 198, 178,
              178, 198, 198, 198, 198, 198, 198, 178,
              178, 198, 208, 218, 218, 208, 198, 178,
              178, 198, 218, 238, 238, 218, 198, 178,
              178, 198, 208, 218, 218, 208, 198, 178,
              178, 198, 198, 198, 198, 198, 198, 178,
              198, 198, 198, 198, 198, 198, 198, 198,]

knight_table = [627, 762, 786, 798, 798, 786, 762, 627,
                763, 798, 822, 834, 834, 822, 798, 763,
                817, 852, 876, 888, 888, 876, 852, 817,
                797, 832, 856, 868, 868, 856, 832, 797,
                799, 834, 858, 870, 870, 858, 834, 799,
                758, 793, 817, 829, 829, 817, 793, 758,
                739, 774, 798, 810, 810, 798, 774, 739,
                683, 718, 742, 754, 754, 742, 718, 683,]

bishop_table = [797, 824, 817, 808, 808, 817, 824, 797,
                814, 841, 834, 825, 825, 834, 841, 814, 0,
                818, 845, 838, 829, 829, 838, 845, 818,
                824, 851, 844, 835, 835, 844, 851, 824,
                827, 854, 847, 838, 838, 847, 854, 827,
                826, 853, 846, 837, 837, 846, 853, 826,
                817, 844, 837, 828, 828, 837, 844, 817,
                792, 819, 812, 803, 803, 812, 819, 792,]

rook_table = [1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258,
              1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258,
             1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258,
             1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258,
              1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258,
              1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258,
              1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258,
              1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258]

queen_table = [2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529,
        2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529,
        2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529,
        2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529,
        2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529,
        2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529,
        2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529,
        2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529]

king_table_open = [60098, 60132, 60073, 60025, 60025, 60073, 60132, 60098,
                   60119, 60153, 60094, 60046, 60046, 60094, 60153, 60119,
                   60146, 60180, 60121, 60073, 60073, 60121, 60180, 60146,
                   60173, 60207, 60148, 60100, 60100, 60148, 60207, 60173,
                   60196, 60230, 60171, 60123, 60123, 60171, 60230, 60196,
                   60224, 60258, 60199, 60151, 60151, 60199, 60258, 60224,
                   60287, 60321, 60262, 60214, 60214, 60262, 60321, 60287,
                   60298, 60332, 60273, 60225, 60225, 60273, 60332, 60298]

king_table_end = [60098, 60132, 60073, 60025, 60025, 60073, 60132, 60098,
                   60119, 60153, 60094, 60046, 60046, 60094, 60153, 60119,
                   60146, 60180, 60121, 60073, 60073, 60121, 60180, 60146,
                   60173, 60207, 60148, 60100, 60100, 60148, 60207, 60173,
                   60196, 60230, 60171, 60123, 60123, 60171, 60230, 60196,
                   60224, 60258, 60199, 60151, 60151, 60199, 60258, 60224,
                   60287, 60321, 60262, 60214, 60214, 60262, 60321, 60287,
                   60298, 60332, 60273, 60225, 60225, 60273, 60332, 60298]


def pos_eval(board, color, endgame):
    score = 0

    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    for piece in piece_types:
        piece_squares = board.pieces(piece, color)
        for square in piece_squares:
            if color is chess.BLACK:
                square = flip(square)

            if piece is chess.PAWN:
                score += pawn_table[square]
            elif piece is chess.KNIGHT:
                score += knight_table[square]
            elif piece is chess.BISHOP:
                score += bishop_table[square]
            elif piece is chess.ROOK:
                score += rook_table[square]
            elif piece is chess.QUEEN:
                score += queen_table[square]
            elif piece is chess.KING and endgame:
                score += king_table_end[square]
            elif piece is chess.KING:
                score += king_table_open[square]

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

def num_controlled_squares(board, color):
    controlled_squares = 0
    for square in chess.SQUARES:
        if len(board.attackers(color, square)) > len(board.attackers(not color, square)):
            controlled_squares += 1
    return controlled_squares

def naive_mob_score(board):
    return len(list(board.legal_moves))

# finds controlled square advantage
def mob_eval(board, color):
    return num_controlled_squares(board, color) - 32
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
        score -= 1.0
    score -= num_doubled_pawns * 1.0
    score -= num_pawn_rams * 1.0
    score -= num_isolated_pawns * 1.0
    score += num_passed_pawns * 1.0

    return score

# get row, column from 0-63 square value
def xy_square(square):
    x = (square % 8) + 1
    y = (square / 8) + 1
    return x, y

# king safety evaluation feature
def ks_eval(board, color):
    tropism_score = 0

    # tropism
    king = 0
    kings = board.pieces(chess.KING, chess.WHITE)
    for square in kings:
        king = square

    k_x, k_y = xy_square(king)
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    for piece in piece_types:
        piece_squares = board.pieces(piece, color)
        for square in piece_squares:
            a_x, a_y = xy_square(square)
            inv_man_dist = 14 - abs(a_x - k_x) + abs(a_y - k_y)
            if piece is chess.PAWN:
                tropism_score -= inv_man_dist * 0.1
            elif piece is chess.KNIGHT:
                tropism_score -= inv_man_dist * 0.5
            elif piece is chess.BISHOP:
                tropism_score -= inv_man_dist * 1.0
            elif piece is chess.ROOK:
                tropism_score -= inv_man_dist * 0.5
            elif piece is chess.QUEEN:
                tropism_score -= inv_man_dist * 2.0

    # pawn shield
    front_adjacent = [king - 9, king - 8, king - 7]
    side_adjacent = [king - 1, king + 1]
    behind_adjacent = [king + 7, king + 8, king + 9]
    pawn_shield = 0

    w_pawns = board.pieces(chess.PAWN, chess.WHITE)
    for pawn in w_pawns:
        if pawn in front_adjacent:
            pawn_shield += 3
        elif pawn in side_adjacent:
            pawn_shield += 2
        elif pawn in behind_adjacent:
            pawn_shield += 1
    # print "pawn shield is: " + str(pawn_shield)

    return tropism_score * 0.3 + pawn_shield * 1.0


class Evaluator():
    def __init__(self, verbose=False):
        self._pos_dict = {}
        self.verbose = verbose

    def num_major_pieces(self, board):
        pieces = 0
        for square in chess.SQUARES:
            if board.piece_at(square) is not None:
                if board.piece_at(square).piece_type is not chess.PAWN:
                    pieces += 1
        return pieces

    def openinggame_eval(self, board):
        score = 0

        mat_score = material_score(board, chess.WHITE) - material_score(board, chess.BLACK)
        pos_score = pos_eval(board, chess.WHITE, False) - pos_eval(board, chess.BLACK, False)
        mob_score = mob_eval(board, chess.WHITE)
        ps_score = ps_eval(board, chess.WHITE)

        feature_scores = [mat_score, pos_score, mob_score, ps_score]
        # normalized_scores = [float(i)/sum(feature_scores) for i in feature_scores]
        feature_weights = [9.0, 0.01, 1.0, 3.0, 1.0]

        if self.verbose:
            print "OPENING"
            print "material score : " + str(mat_score)
            print "positional score : " + str(pos_score)
            print "mobility score : " + str(mob_score)
            print "pawn structure score : " + str(ps_score)

        for i in range(len(feature_scores)):
            score += feature_scores[i] * feature_weights[i]

        return score

    def middlegame_eval(self, board):
        score = 0

        mat_score = material_score(board, chess.WHITE) - material_score(board, chess.BLACK)
        pos_score = pos_eval(board, chess.WHITE, False) - pos_eval(board, chess.BLACK, False)
        mob_score = mob_eval(board, chess.WHITE)
        ps_score = ps_eval(board, chess.WHITE)
        ks_score = ks_eval(board, chess.WHITE) - ks_eval(board, chess.BLACK)

        feature_scores = [mat_score, pos_score, mob_score, ps_score, ks_score]
        # normalized_scores = [float(i)/sum(feature_scores) for i in feature_scores]
        feature_weights = [8.0, 0.01, 1.0, 3.0, 1.0]

        if self.verbose:
            print "MIDDLEGAME"
            print "material score : " + str(mat_score)
            print "positional score : " + str(pos_score)
            print "mobility score : " + str(mob_score)
            print "pawn structure score : " + str(ps_score)
            print "king safety score : " + str(ks_score)

        for i in range(len(feature_scores)):
            print str(feature_scores[i] * feature_weights[i])
            score += feature_scores[i] * feature_weights[i]

        if board.is_check():
            score += 20

        return score

    def endgame_eval(self, board):
        score = 0

        mat_score = material_score(board, chess.WHITE) - material_score(board, chess.BLACK)
        pos_score = pos_eval(board, chess.WHITE, False) - pos_eval(board, chess.BLACK, False)
        mob_score = mob_eval(board, chess.WHITE)
        ps_score = ps_eval(board, chess.WHITE)
        ks_score = ks_eval(board, chess.WHITE) - ks_eval(board, chess.BLACK)

        if self.verbose:
            print "ENDGAME"
            print "material score : " + str(mat_score)
            print "positional score : " + str(pos_score)
            print "mobility score : " + str(mob_score)
            print "pawn structure score : " + str(ps_score)
            print "king safety score : " + str(ks_score)

        feature_scores = [mat_score, pos_score, mob_score, ps_score, ks_score]
        # normalized_scores = [float(i)/sum(feature_scores) for i in feature_scores]
        feature_weights = [10.0, 2.0, 3.0, 2.0, 2.0]

        # TODO: include pawn advantage

        for i in range(len(feature_scores)):
            score += feature_scores[i] * feature_weights[i]

        if board.is_check():
            score += 15

        return score

    # returns evaluation score for white
    def evaluate(self, board):
        if board.zobrist_hash() in self._pos_dict:
            return self._pos_dict.get(board.zobrist_hash)

        if board.is_game_over():
            if board.result() == "0-1":
                return black_win_value
            if board.result() == "1-0":
                return white_win_value
            else:
                return 0

        # return material_score(board, chess.WHITE) - material_score(board, chess.BLACK)

        if self.num_major_pieces(board) > 12:
            score = self.openinggame_eval(board)
        elif self.num_major_pieces(board) > 7:
            score = self.middlegame_eval(board)
        else:
            score = self.endgame_eval(board)

        self._pos_dict[board.zobrist_hash] = score
        return score


if __name__ == '__main__':
    # print(xy_square(63))
    e = Evaluator(verbose=True)
    # e.evaluate(chess.Board())
    print(e.evaluate(chess.Board('1k1r1b1r/pp3ppp/3p4/2p1p3/6n1/1NB2N2/1P1KP1PP/1q3B1R b KQkq - 0 1')))
    print(e.evaluate(chess.Board('1k1r1b1r/pp3ppp/3p4/2p1p3/6P1/1NB2N2/1P1KP1P1/1q3BR1 b k - 0 1')))

