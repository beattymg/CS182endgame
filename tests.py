# CS182 Deep Crimson: Matthew Beatty and Akshay Saini
# tests.py
# This file includes testing for the search and evaluation
# components of our agents using various chess scenarios

import chess
import chess.polyglot
from evaluator import Evaluator
import main

# Tests for search correctness
def test_search():
    agent = main.NegamaxAgent(chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15"), max_time=300,\
                         transposition_table=True, abpruning=True)
    agent.search()

    print "TACTIC 1"
    test_board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
    print "\nTACTIC 2"
    test_board = chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15")
    print "\nTACTIC 3"
    test_board = chess.Board("rn1q1rk1/ppp1b1pp/3pP3/3p4/3P1B2/5NP1/PPP4P/R2Q1K1R b - - 0 13")
    print "\nTACTIC 4"
    test_board = chess.Board("5k2/6pp/R2P1p2/4p3/pr2P3/5P1P/8/6K1 w - - 1 33")

# Various assertion tests for the evaluation functionality
def test_eval():
    e = Evaluator(verbose=False)
    assert e.xy_square(63) == (8,8)
    # print(e.evaluate(chess.Board('1k1r1b1r/pp3ppp/3p4/2p1p3/6n1/1NB2N2/1P1KP1PP/1q3B1R b KQkq - 0 1')))
    # print(e.evaluate(chess.Board('1k1r1b1r/pp3ppp/3p4/2p1p3/6P1/1NB2N2/1P1KP1P1/1q3BR1 b k - 0 1')))
    # print(e.evaluate(chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")))

    starting_mat = e.material_score(chess.Board(), chess.WHITE) - e.material_score(chess.Board(), chess.BLACK)
    assert starting_mat == 0.0

    # Second should be better
    test_1 = e.evaluate(chess.Board('r1bq1rk1/pppp1ppp/4p3/8/1b2P3/2N2N2/PPPPQPPP/R1B1KB1R b k - 0 1'))
    test_2 = e.evaluate(chess.Board('r1bq1rk1/pppp1ppp/4p3/8/1b2P3/P1N2N2/1PPPQPPP/1RB1KB1R b k - 0 1'))
    assert test_2 > test_1

    # Second should be better
    test_3 = e.evaluate(chess.Board('r1bqk2r/pppp1ppp/2n1pn2/8/4P3/2b2N2/PPPP1PPP/1RBQKB1R b k - 0 1'))
    test_4 = e.evaluate(chess.Board('r1bqk2r/pppp1ppp/2n1pn2/8/4P3/2P2N2/P1PP1PPP/R1BQKB1R b k - 0 1'))
    assert test_4 > test_3

    board = chess.Board('r1bk3r/ppppQppp/n3pn2/8/4P3/B1b2N2/PPPP1PPP/1R2KB1R b k - 0 1')
    assert board.is_game_over()

    # f5d5 should evaluate to the best move
    board = chess.Board('6k1/3p3p/P4B2/8/5b2/3R2P1/5P2/1K6 w KQkq - 0 1')
    for move in board.legal_moves:
        board.push(move)
        print "MOVE:" + str(move)
        print(e.evaluate(board))
        board.pop()


if __name__ == '__main__':
    test_eval()

