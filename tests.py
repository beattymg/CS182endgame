import chess
import chess.polyglot
from timeit import default_timer as timer
import random
import evals
from evaluator import Evaluator
import main


def test_search():
    agent = main.DeepCrimsonAgent(chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15"), max_time=300, \
                                  transposition_table=True, abpruning=True)
    agent.negamax_search()

    print "TACTIC 1"
    test_board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
    print "\nTACTIC 2"
    test_board = chess.Board("r1b1k1r1/p1pq1p2/1p1p1npp/3Pp3/2P4N/2PBP3/P1Q2PPP/R4RK1 b q - 3 15")
    print "\nTACTIC 3"
    test_board = chess.Board("rn1q1rk1/ppp1b1pp/3pP3/3p4/3P1B2/5NP1/PPP4P/R2Q1K1R b - - 0 13")
    print "\nTACTIC 4"
    test_board = chess.Board("5k2/6pp/R2P1p2/4p3/pr2P3/5P1P/8/6K1 w - - 1 33")


def test_eval():
    e = Evaluator(verbose=True)
    # print(e.evaluate(chess.Board('1k1r1b1r/pp3ppp/3p4/2p1p3/6n1/1NB2N2/1P1KP1PP/1q3B1R b KQkq - 0 1')))
    # print(e.evaluate(chess.Board('1k1r1b1r/pp3ppp/3p4/2p1p3/6P1/1NB2N2/1P1KP1P1/1q3BR1 b k - 0 1')))
    # print(e.evaluate(chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")))
    starting_mat = e.material_score(chess.Board(), chess.WHITE) - e.material_score(chess.Board(), chess.BLACK)
    assert starting_mat == 0.0


if __name__ == '__main__':
    test_eval()

