import chess
import chess.polyglot
from timeit import default_timer as timer
from evaluator import Evaluator, SimpleEvaluator


class NodeType:
    EXACT = 1   # nodes whose value was exactly calculated
    ALPHA = 2   # nodes with a value lower than the lower-bound alpha
    BETA = 3    # nodes with a value higher than the upper-bound beta


class EvalType:
    SIMPLE = 1   # nodes whose value was exactly calculated
    COMPLEX = 2   # nodes with a value lower than the lower-bound alpha


class TableEntry:
    def __init__(self, zobrist_key, best_move, depth, value, node_type):
        self.zobrist_key = zobrist_key
        self.best_move = best_move
        self.depth = depth
        self.value = value
        self.node_type = node_type


# an iterative deepening minimax agent that can use alpha-beta and transposition tables to prune nodes
class DeepCrimsonAgent():
    def __init__(self, board, max_depth, evaluation_type, abpruning=True, transposition_table=True, table_size=2**20, verbose=False):
        # initialize board
        self.board = board

        # initialize max time allowed
        self.max_depth = max_depth

        # choose evaluation function
        if evaluation_type == EvalType.SIMPLE:
            self.evaluator = SimpleEvaluator()
        elif evaluation_type == EvalType.COMPLEX:
            self.evaluator = Evaluator(verbose=False)

        # choose whether or not to alpha-beta prune
        self.abpruning = abpruning

        # set up transposition table
        self.transposition_table = transposition_table
        self.TABLE_SIZE = table_size
        if transposition_table:
            self.tt = [None] * table_size

        # print output if necessary
        self.verbose = verbose

    # returns the negamax value of the current board state
    def negamax_value(self, depth, alpha, beta, color):
        if depth == 0 or self.board.is_game_over():
            return color * self.evaluator.evaluate(self.board)

        legal_moves = self.board.legal_moves

        # read from the transposition table
        if self.transposition_table:
            key = self.board.zobrist_hash()
            index = key % self.TABLE_SIZE
            old_alpha = alpha

            table_entry = self.tt[index]
            if table_entry is not None and table_entry.zobrist_key == key:
                if table_entry.depth >= depth:
                    if table_entry.node_type == NodeType.EXACT:
                        return table_entry.value
                    elif table_entry.node_type == NodeType.BETA:
                        alpha = max(alpha, table_entry.value)
                    elif table_entry.node_type == NodeType.ALPHA:
                        beta = min(beta, table_entry.value)
                    if alpha >= beta:
                        return table_entry.value
                if table_entry.best_move in legal_moves:
                    legal_moves = list(legal_moves)
                    legal_moves.insert(0, legal_moves.pop(legal_moves.index(table_entry.best_move)))

        best_value = float("-inf")
        best_move = None
        for move in legal_moves:
            self.nodes += 1
            self.board.push(move)
            v = -self.negamax_value(depth - 1, -beta, -alpha, -color)
            self.board.pop()
            if v > best_value:
                best_value = v
                best_move = move
            if self.abpruning:
                alpha = max(alpha, v)
                if alpha >= beta:
                    break

        # write to the transposition table
        if self.transposition_table:
            if best_move <= old_alpha:
                node_type = NodeType.ALPHA
            elif best_value >= beta:
                node_type = NodeType.BETA
            else:
                node_type = NodeType.EXACT
            self.tt[index] = TableEntry(key, best_move, depth, best_value, node_type)

        return best_value

    # returns the move associated with the highest negamax value
    def negamax_search(self):
        color = 1 if self.board.turn else -1
        for depth in range(1, self.max_depth):
            iter_start = timer()
            depth += 1
            alpha = float("-inf")
            beta = float("+inf")
            best_move = None
            best_value = float("-inf")
            self.nodes = 0

            for move in self.board.legal_moves:
                self.nodes += 1
                self.board.push(move)
                v = -self.negamax_value(depth - 1, -beta, -alpha, -color)
                self.board.pop()
                if self.abpruning:
                    alpha = max(alpha, v)
                if v > best_value:
                    best_value = v
                    best_move = move

            if self.verbose:
                iter_end = timer()
                seconds = iter_end - iter_start
                print
                print str(depth) + "-ply"
                print "nodes", self.nodes
                print "time", seconds
                print "kn/s", self.nodes / 1000.0 / seconds
                print "move", best_move

        return best_move

    # calculates the MTD-(f) value of the current board state
    def mtdf_value(self, f, depth, color):
        g = f
        upper_bound = float("+inf")
        lower_bound = float("-inf")
        while lower_bound < upper_bound:
            beta = max(g, lower_bound+1)
            g = self.negamax_value(depth, beta-1, beta, color)
            if g < beta:
                upper_bound = g
            else:
                lower_bound = g
        return g

    # returns the move associated with the highest MTD-(f) value
    def mtdf_search(self):
        color = 1 if self.board.turn else -1
        key = self.board.zobrist_hash()
        index = key % self.TABLE_SIZE

        f = 0
        for depth in range(1, self.max_depth + 1):
            iter_start = timer()
            self.nodes = 0
            f = self.mtdf_value(f, depth, color)

            if self.verbose:
                iter_end = timer()
                seconds = iter_end - iter_start
                print
                print str(depth) + "-ply"
                print "nodes", self.nodes
                print "time", seconds
                print "kn/s", self.nodes / 1000.0 / seconds
                table_entry = self.tt[index]
                if table_entry is not None and table_entry.zobrist_key == key:
                    print "move", table_entry.best_move
                else:
                    print "move", None
                print "value:", f

        # read best move from transposition table
        table_entry = self.tt[index]
        if table_entry is not None and table_entry.zobrist_key == key:
            return table_entry.best_move
        else:
            print "current position not in transposition table!"
            return None

    # e.g. self.move(self.search()) updates internal board representation with best move found by NegaMax search
    def move(self, move):
        self.board.push(move)


if __name__ == '__main__':
    print "TACTIC 1"
    test_board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
    # print "\nTACTIC 2"
    # test_board = chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15")
    # print "\nTACTIC 3"
    # test_board = chess.Board("rn1q1rk1/ppp1b1pp/3pP3/3p4/3P1B2/5NP1/PPP4P/R2Q1K1R b - - 0 13")
    # print "\nTACTIC 4"
    # test_board = chess.Board("5k2/6pp/R2P1p2/4p3/pr2P3/5P1P/8/6K1 w - - 1 33")

    agent = DeepCrimsonAgent(test_board, max_depth=6, evaluation_type=EvalType.SIMPLE, verbose=True)
    print "Negamax search"
    print "FEN:", test_board.fen()
    move = agent.negamax_search()
    print "Move:", move

    agent = DeepCrimsonAgent(test_board, max_depth=6, evaluation_type=EvalType.SIMPLE, verbose=True)
    print "\nMTD-(f) search"
    print "FEN:", test_board.fen()
    move = agent.mtdf_search()
    print "Move:", move

