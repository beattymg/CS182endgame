# CS182 Deep Crimson: Matthew Beatty and Akshay Saini
# evaluator.py
# This file has the functions and logic for our evaluation functions

import chess
import chess.polyglot
import chess.syzygy

white_win_value = float("inf")
black_win_value = float("-inf")

'''
Below are piece-square tables used in our positional feature to
give the approximate value of that specific piece in a position
'''
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

king_table_open = [-30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                 20, 20,  0,  0,  0,  0, 20, 20,
                 20, 30, 10,  0,  0, 10, 30, 20]

king_table_end = [-50,-40,-30,-20,-20,-30,-40,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50 ]

class Evaluator():
    def __init__(self, verbose=False):
        self._pos_dict = {}
        self.verbose = verbose

    # board positional evaluation feature
    def pos_eval(self, board, color, endgame):
        score = 0

        piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
        for piece in piece_types:
            piece_squares = board.pieces(piece, color)
            for square in piece_squares:
                if color is chess.BLACK:
                    square = self.flip(square)

                # Checks each piece against piece-square table and updates
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
                # Uses different tables for king in middle and endgame
                elif piece is chess.KING and endgame:
                    score += king_table_end[square]
                elif piece is chess.KING:
                    score += king_table_open[square]

        return score

    # Flips orientation of a square for positions for black player
    def flip(self, square):
        return (7 - (square % 8)) + ((7 - (square // 8)) * 8)

    # Returns total number of pieces on the board
    def num_pieces(self, board):
        pieces = 0
        for s in chess.SQUARES:
            if board.piece_at(s):
                pieces += 1
        return pieces

    # Material evaluation feature
    # Uses the weights described by Claude Shannon
    def material_score(self, board, color):
        score = len(board.pieces(chess.PAWN, color))\
               + (3.0 * len(board.pieces(chess.KNIGHT, color)))\
               + (3.0 * len(board.pieces(chess.BISHOP, color)))\
               + (5.0 * len(board.pieces(chess.ROOK, color)))\
               + (9.0 * len(board.pieces(chess.QUEEN, color)))

        if len(board.pieces(chess.BISHOP, color)) == 2:
            score += 2.0
        if len(board.pieces(chess.KNIGHT, color)) == 2:
            score -= 1.0

        return score

    # Returns balance of controlled squares on board
    def num_controlled_squares(self, board, color):
        controlled_squares = 0
        for square in chess.SQUARES:
            if len(board.attackers(color, square)) > len(board.attackers(not color, square)):
                controlled_squares += 1
        return controlled_squares

    def naive_mob_score(self, board):
        return len(list(board.legal_moves))

    # Mobility evaluation featuring using controlled squares
    def mob_eval(self, board, color):
        return self.num_controlled_squares(board, color) - self.num_controlled_squares(board, not color)

    # Pawn structure evaluation featuring using a variety of metrics
    def ps_eval(self, board, color):
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

        # Weighting and 8 pawn penalty
        if (len(w_pawns) > 7):
            score -= 1.0
        score -= num_doubled_pawns * 1.0
        score -= num_pawn_rams * 1.0
        score -= num_isolated_pawns * 1.0
        score += num_passed_pawns * 1.0

        return score

    # Get row, column from 0-63 square value
    def xy_square(self, square):
        x = (square % 8) + 1
        y = (square / 8) + 1
        return x, y

    # Pawn advantage evaluation feature used in the endgame
    def pa_eval(self, board, color):
        p = len(list(board.pieces(chess.PAWN, color))) - len(list(board.pieces(chess.PAWN, not color)))
        return 1.0 / (1.0 + (10.0 ** (-p / 4.0)))

    # King safety evaluation feature
    def ks_eval(self, board, color):
        tropism_score = 0

        # Tropism: finds value for the distance of the king from attackers
        king = 0
        kings = board.pieces(chess.KING, color)
        for square in kings:
            king = square
        k_x, k_y = self.xy_square(king)
        piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
        for piece in piece_types:
            piece_squares = board.pieces(piece, color)
            for square in piece_squares:
                a_x, a_y = self.xy_square(square)
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

        # Pawn shield: finds whether king is protected by pawns
        front_adjacent = [king - 9, king - 8, king - 7]
        side_adjacent = [king - 1, king + 1]
        behind_adjacent = [king + 7, king + 8, king + 9]
        pawn_shield = 0
        w_pawns = board.pieces(chess.PAWN, color)
        for pawn in w_pawns:
            if pawn in front_adjacent:
                pawn_shield += 3
            elif pawn in side_adjacent:
                pawn_shield += 2
            elif pawn in behind_adjacent:
                pawn_shield += 1

        return tropism_score * 0.3 + pawn_shield * 1.0

    def num_major_pieces(self, board):
        pieces = 0
        for square in chess.SQUARES:
            if board.piece_at(square) is not None:
                if board.piece_at(square).piece_type is not chess.PAWN:
                    pieces += 1
        return pieces

    # Evaluation function for opening game
    def openinggame_eval(self, board):
        score = 0

        # Calculates feature scores
        mat_score = self.material_score(board, chess.WHITE) - self.material_score(board, chess.BLACK)
        pos_score = self.pos_eval(board, chess.WHITE, False) - self.pos_eval(board, chess.BLACK, False)
        mob_score = self.mob_eval(board, chess.WHITE)
        ps_score = self.ps_eval(board, chess.WHITE) - self.ps_eval(board, chess.BLACK)

        # Assigns feature weights
        feature_scores = [mat_score, pos_score, mob_score, ps_score]
        feature_weights = [1.5, 0.001, 0.0005, 0.03]

        if self.verbose:
            print "OPENING"
            print "material score : " + str(mat_score)
            print "positional score : " + str(pos_score)
            print "mobility score : " + str(mob_score)
            print "pawn structure score : " + str(ps_score)

        # Sets score as linear combination of features and their weights
        for i in range(len(feature_scores)):
            score += feature_scores[i] * feature_weights[i]

        return score

    # Evaluation function for middlegame
    def middlegame_eval(self, board):
        score = 0

        # Calculates feature scores
        mat_score = self.material_score(board, chess.WHITE) - self.material_score(board, chess.BLACK)
        pos_score = self.pos_eval(board, chess.WHITE, False) - self.pos_eval(board, chess.BLACK, False)
        mob_score = self.mob_eval(board, chess.WHITE)
        ps_score = self.ps_eval(board, chess.WHITE) - self.ps_eval(board, chess.BLACK)
        ks_score = self.ks_eval(board, chess.WHITE) - self.ks_eval(board, chess.BLACK)

        # Assigns feature weights
        feature_scores = [mat_score, pos_score, mob_score, ps_score, ks_score]
        feature_weights = [1.5, 0.002, 0.0005, 0.05, 0.04]

        if self.verbose:
            print "MIDDLEGAME"
            print "material score : " + str(mat_score)
            print "positional score : " + str(pos_score)
            print "mobility score : " + str(mob_score)
            print "pawn structure score : " + str(ps_score)
            print "king safety score : " + str(ks_score)

        # Sets score as linear combination of features and their weights
        for i in range(len(feature_scores)):
            score += feature_scores[i] * feature_weights[i]

        return score

    # Evaluation function for endgame
    def endgame_eval(self, board):
        score = 0

        # Calculates feature scores
        mat_score = self.material_score(board, chess.WHITE) - self.material_score(board, chess.BLACK)
        pos_score = self.pos_eval(board, chess.WHITE, False) - self.pos_eval(board, chess.BLACK, False)
        mob_score = self.mob_eval(board, chess.WHITE)
        ps_score = self.ps_eval(board, chess.WHITE) - self.ps_eval(board, chess.BLACK)
        ks_score = self.ks_eval(board, chess.WHITE) - self.ks_eval(board, chess.BLACK)
        pa_score = self.pa_eval(board, chess.WHITE)

        if self.verbose:
            print "ENDGAME"
            print "material score : " + str(mat_score)
            print "positional score : " + str(pos_score)
            print "mobility score : " + str(mob_score)
            print "pawn structure score : " + str(ps_score)
            print "king safety score : " + str(ks_score)

        # Assigns feature weights
        feature_scores = [mat_score, pos_score, mob_score, ps_score, ks_score, pa_score]
        feature_weights = [1.5, 0.001, 0.0001, 0.06, 0.07, 0.1]

        # Sets score as linear combination of features and their weights
        for i in range(len(feature_scores)):
            score += feature_scores[i] * feature_weights[i]

        return score

    # Evaluation called from agents
    def evaluate(self, board):
        # Checks if position has already been evaluated
        if board.zobrist_hash() in self._pos_dict:
            # Returns score from dictionary
            return self._pos_dict.get(board.zobrist_hash)

        # Checks for game over conditions
        if board.is_game_over():
            if board.result() == "0-1":
                return black_win_value
            if board.result() == "1-0":
                return white_win_value
            else:
                return 0

        # Depending on game phase, evaluates the board differently
        if self.num_major_pieces(board) > 12:
            score = self.openinggame_eval(board)
        elif self.num_major_pieces(board) > 7:
            score = self.middlegame_eval(board)
        else:
            score = self.endgame_eval(board)

        # Adds position score to dictionary
        self._pos_dict[board.zobrist_hash] = score
        return score


if __name__ == '__main__':
    e = Evaluator(verbose=True)
    print(e.evaluate(chess.Board()))
