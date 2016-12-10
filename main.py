import chess
import chess.polyglot
from timeit import default_timer as timer
import random
import evals
from evaluator import Evaluator


class NodeType:
    EXACT = 1   # nodes whose value was exactly calculated
    ALPHA = 2   # nodes with a value lower than the lower-bound alpha
    BETA = 3    # nodes with a value higher than the upper-bound beta


class TableEntry:
    def __init__(self, zobrist_key, best_move, depth, value, node_type):
        self.zobrist_key = zobrist_key
        self.best_move = best_move
        self.depth = depth
        self.value = value
        self.node_type = node_type


# an iterative deepening minimax agent that can use alpha-beta and transposition tables to prune nodes
class NegamaxAgent():
    def __init__(self, board, max_time, abpruning=True, transposition_table=True, table_size=2**16, verbose=True):
        self.board = board
        self.max_time = max_time
        self.abpruning = abpruning
        self.transposition_table = transposition_table
        self.TABLE_SIZE = 2**16
        if transposition_table:
            self.tt = [None] * table_size
        self.verbose = verbose
        self.evaluator = Evaluator()

    def negamax(self, depth, alpha, beta, color):
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
            v = -self.negamax(depth - 1, -beta, -alpha, -color)
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

    def search(self):
        color = 1 if self.board.turn else -1

        depth = 1
        start = timer()
        while timer() - start <= self.max_time:
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
                v = -self.negamax(depth - 1, -beta, -alpha, -color)
                self.board.pop()
                if self.abpruning:
                    alpha = max(alpha, v)
                if v > best_value:
                    best_value = v
                    best_move = move
                if timer() - start > self.max_time:
                    break

            if self.verbose:
                iter_end = timer()
                seconds = iter_end - iter_start
                print
                print str(depth) + "-ply"
                print "nodes", self.nodes
                print "time", seconds
                print "kn/s", self.nodes / 1000.0 / seconds
                print "move", best_move

        if best_move is None:
            legal_moves = list(self.board.legal_moves)
            return legal_moves[random.randint(0, len(legal_moves) - 1)]
        else:
            return best_move

    # e.g. self.move(self.search()) updates internal board representation with best move found by NegaMax search
    def move(self, move):
        self.board.push(move)


def search_with_opening_book(board):
    reader = chess.polyglot.open_reader('komodo.bin')
    moves = []
    for entry in reader.find_all(board):
        if entry.move() in board.legal_moves:
            moves.append(entry.move())

    if not moves:
        return chess.Move.null()
    else:
        return random.choice(moves)


if __name__ == '__main__':
    agent = NegamaxAgent(chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15"), max_time=300,\
                         transposition_table=True, abpruning=True)
    agent.search()

    # print "TACTIC 1"
    # test_board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
    # print "\nTACTIC 2"
    # test_board = chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15")
    # print "\nTACTIC 3"
    # test_board = chess.Board("rn1q1rk1/ppp1b1pp/3pP3/3p4/3P1B2/5NP1/PPP4P/R2Q1K1R b - - 0 13")
    # print "\nTACTIC 4"
    # test_board = chess.Board("5k2/6pp/R2P1p2/4p3/pr2P3/5P1P/8/6K1 w - - 1 33")
