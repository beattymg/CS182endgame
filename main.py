import chess
import chess.polyglot
from timeit import default_timer as timer
import random
import evals

my_globals = {'nodes': 0}
abpruning = True
transposition_table = True
TABLE_SIZE = 2**16
tt = [None] * TABLE_SIZE


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


def negamax(board, depth, alpha, beta, color):
    if depth == 0 or board.is_game_over():
        return color * evals.evaluate(board)

    legal_moves = board.legal_moves

    # read from the transposition table
    if transposition_table:
        key = board.zobrist_hash()
        index = key % TABLE_SIZE
        old_alpha = alpha

        ttEntry = tt[index]
        if ttEntry is not None and ttEntry.zobrist_key == key:
            if ttEntry.depth >= depth:
                if ttEntry.node_type == NodeType.EXACT:
                    return ttEntry.value
                elif ttEntry.node_type == NodeType.BETA:
                    alpha = max(alpha, ttEntry.value)
                elif ttEntry.node_type == NodeType.ALPHA:
                    beta = min(beta, ttEntry.value)
                if alpha >= beta:
                    return ttEntry.value
            if ttEntry.best_move in legal_moves:
                legal_moves = list(legal_moves)
                legal_moves.insert(0, legal_moves.pop(legal_moves.index(ttEntry.best_move)))

    best_value = float("-inf")
    best_move = None
    for move in legal_moves:
        board.push(move)
        my_globals['nodes'] += 1
        v = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()
        if v > best_value:
            best_value = v
            best_move = move
        if abpruning:
            alpha = max(alpha, v)
            if alpha >= beta:
                break

    # write to the transposition table
    if transposition_table:
        if best_move <= old_alpha:
            node_type = NodeType.ALPHA
        elif best_value >= beta:
            node_type = NodeType.BETA
        else:
            node_type = NodeType.EXACT
        tt[index] = TableEntry(key, best_move, depth, best_value, node_type)

    return best_value


def search(board, depth):
    color = 1 if board.turn else -1
    alpha = float("-inf")
    beta = float("+inf")

    start = timer()
    my_globals['nodes'] = 0

    best_move = None
    best_value = float("-inf")
    for move in board.legal_moves:
        board.push(move)
        my_globals['nodes'] += 1
        v = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()
        if abpruning:
            alpha = max(alpha, v)
        if v > best_value:
            best_value = v
            best_move = move
    end = timer()
    seconds = end - start
    print "nodes", my_globals['nodes']
    print "time", seconds
    print "kn/s", my_globals['nodes'] / 1000.0 / seconds
    print "move",

    # if move is None:
    #     legal_moves = list(board.legal_moves)
    #     return legal_moves[random.randint(0, len(legal_moves) - 1)]
    # else:
    return best_move


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
    print "TACTIC 1"
    test_board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
    print "\n2-ply"
    print search(test_board, 2)
    print "\n3-ply"
    print search(test_board, 3)
    print "\n4-ply"
    print search(test_board, 4)
    print "\n5-ply"
    print search(test_board, 5)

    print "\nTACTIC 2"
    test_board = chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15")
    print "\n2-ply"
    print search(test_board, 2)
    print "\n3-ply"
    print search(test_board, 3)
    print "\n4-ply"
    print search(test_board, 4)
    print "\n5-ply"
    print search(test_board, 5)

    print "\nTACTIC 3"
    test_board = chess.Board("rn1q1rk1/ppp1b1pp/3pP3/3p4/3P1B2/5NP1/PPP4P/R2Q1K1R b - - 0 13")
    print "\n2-ply"
    print search(test_board, 2)
    print "\n3-ply"
    print search(test_board, 3)
    print "\n4-ply"
    print search(test_board, 4)
    print "\n5-ply"
    print search(test_board, 5)

    print "\nTACTIC 4"
    test_board = chess.Board("5k2/6pp/R2P1p2/4p3/pr2P3/5P1P/8/6K1 w - - 1 33")
    print "\n2-ply"
    print search(test_board, 2)
    print "\n3-ply"
    print search(test_board, 3)
    print "\n4-ply"
    print search(test_board, 4)
    print "\n5-ply"
    print search(test_board, 5)
