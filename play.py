
import math
import chess, chess.pgn
import chess.uci
import sunfish
import heapq
import time
import re
import string
import numpy
import pickle
import random
import traceback

def create_move(board, crdn):
    # workaround for pawn promotions
    move = chess.Move.from_uci(crdn)
    if board.piece_at(move.from_square).piece_type == chess.PAWN:
        if int(move.to_square/8) in [0, 7]:
            move.promotion = chess.QUEEN # always promote to queen
    return move

class Player(object):
    def move(self, gn_current):
        raise NotImplementedError()

class RLPlayer(Player):
    def move(self, gn_current):
        raise NotImplementedError()

class MinimaxPlayer(Player):
    def move(self, gn_current):
        raise NotImplementedError()

class Sunfish(Player):
    def __init__(self, maxn=1e4):
        self._pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0)
        self._maxn = maxn

    def move(self, gn_current):
        searcher = sunfish.Searcher()

        assert(gn_current.board().turn == False)

        # Apply last_move
        crdn = str(gn_current.move)
        move = (sunfish.parse(crdn[0:2]), sunfish.parse(crdn[2:4]))
        self._pos = self._pos.move(move)

        t0 = time.time()
        move, score = searcher.search(self._pos, self._maxn)
        print time.time() - t0, move, score
        self._pos = self._pos.move(move)

        crdn = sunfish.render(119-move[0]) + sunfish.render(119 - move[1])
        move = create_move(gn_current.board(), crdn)

        gn_new = chess.pgn.GameNode()
        gn_new.parent = gn_current
        gn_new.move = move

        return gn_new

class Human(Player):
    def move(self, gn_current):
        bb = gn_current.board()

        print bb

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

def play():
    gn_current = chess.pgn.Game()

    player_a = Human()
    player_b = Sunfish(maxn=10)

    times = {'A': 0.0, 'B': 0.0}

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

            times[side] += time.time() - t0
            print '=========== Player %s: %s' % (side, gn_current.move)
            s = str(gn_current.board())

            if gn_current.board().is_checkmate():
                return side, times
            elif gn_current.board().is_stalemate():
                return '-', times
            elif gn_current.board().can_claim_fifty_moves():
                return '-', times
            elif s.find('K') == -1 or s.find('k') == -1:
                return side, times

if __name__ == '__main__':
    play()
