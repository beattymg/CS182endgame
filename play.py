import time
import traceback

import random
import chess
import chess.pgn
import chess.uci

import sunfish

import main

def create_move(board, crdn):
    move = chess.Move.from_uci(crdn)
    if board.piece_at(move.from_square).piece_type == chess.PAWN:
        if int(move.to_square/8) in [0, 7]:
            move.promotion = chess.QUEEN
    return move

class Player(object):
    def move(self, gn_current):
        raise NotImplementedError()

class RLPlayer(Player):
    def move(self, gn_current):
        raise NotImplementedError()

class Sunfish(Player):
    def __init__(self, maxn=1e4, dumb=False):
        self._pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0)
        self._maxn = maxn
        if dumb:
            sunfish.set_pst()

    def move(self, gn_current):
        searcher = sunfish.Searcher()

        assert(gn_current.board().turn == False)

        # print str(gn_current.board())
        # Apply last_move
        crdn = str(gn_current.move)
        move = (sunfish.parse(crdn[0:2]), sunfish.parse(crdn[2:4]))
        self._pos = self._pos.move(move)

        t0 = time.time()
        move, score = searcher.search(self._pos, self._maxn)
        # print "move and score is\n"
        # print move, score
        print time.time() - t0, move, score
        self._pos = self._pos.move(move)

        crdn = sunfish.render(119-move[0]) + sunfish.render(119 - move[1])
        move = create_move(gn_current.board(), crdn)

        gn_new = chess.pgn.GameNode()
        gn_new.parent = gn_current
        gn_new.move = move

        return gn_new

class Human(Player):
    def __init__(self, maxn=1e4):
        self._pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0)
        self._maxn = maxn

    def move(self, gn_current):
        bb = gn_current.board()

        # print bb

        def get_move(move_str):
            try:
                move = chess.Move.from_uci(move_str)
            except:
                print 'cant parse'
                return False
            if move not in bb.legal_moves:
                print 'not a legal move'
                return False
            else:
                return move

        while True:
            print 'your turn:'
            move = get_move(raw_input())
            if move:
                break

        gn_new = chess.pgn.GameNode()
        gn_new.parent = gn_current
        gn_new.move = move

        return gn_new


class Random(Player):
    def __init__(self, maxn=2):
        return

    def move(self, gn_current):
        return

class MinimaxPlayer(Player):
    def __init__(self, time, verbose, depth=2, opening_book=True):
        self._depth = depth
        self._opening_book = opening_book
        self._negamax = main.DeepCrimsonAgent(chess.Board(), max_time=time, evaluation_type=main.EvalType.MATERIAL, \
                                              transposition_table=True, abpruning=True, verbose=verbose)

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

    def move(self, gn_current):
        assert gn_current.board().turn is True

        # print str(gn_current.board())

        board = gn_current.board()
        self._negamax.board = board
        t0 = time.time()

        if self._opening_book:
            uci_move = str(self.search_with_opening_book(board))
            if uci_move == "0000":
                self._opening_book = False
                uci_move = str(self._negamax.negamax_search())
        else:
            uci_move = str(self._negamax.negamax_search())

        move = create_move(gn_current.board(), uci_move)
        print time.time() - t0, move

        gn_new = chess.pgn.GameNode()
        gn_new.parent = gn_current
        gn_new.move = move

        # print str(gn_new.board())

        return gn_new


def play():
    gn_current = chess.pgn.Game()

    player_a = MinimaxPlayer(10, True, depth=0)
    # player_b = Sunfish(maxn=0, dumb=False)
    player_b = Human()

    times = {'A': 0.0, 'B': 0.0}
    move_count = 0

    print "NEW GAME\n"

    while True:
        for side, player in [('A', player_a), ('B', player_b)]:
            t0 = time.time()
            try:
                gn_current = player.move(gn_current)
            except KeyboardInterrupt:
                return
            except:
                traceback.print_exc()
                return side + '-exception', times

            move_count += 1
            times[side] += time.time() - t0
            print '=========== Player %s: %s' % (side, gn_current.move)
            s = str(gn_current.board())
            print s
            print "total moves in game: " + str(move_count)

            if gn_current.board().is_checkmate():
                return side, times, move_count
            elif gn_current.board().is_stalemate():
                return '-', times
            elif gn_current.board().can_claim_fifty_moves():
                return '-', times
            elif s.find('K') == -1 or s.find('k') == -1:
                return side, times, move_count

def play_games(num_games):
    open('games.txt', 'w').close()
    f = open('games.txt', 'a')
    f.write(str(num_games) + " GAMES BETWEEN MINIMAX AND SUNFISH AGENTS\n")
    for _ in range(num_games):
        results = list(play())
        f.write(str(results[0]) + " " + str(results[1]) + " " + str(results[2]) + "\n")
    f.close()


if __name__ == '__main__':
    # play_games(5)
    play()

