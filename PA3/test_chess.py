# Wesley Tan
# COSC 76
# PA3: Chess AI

# pip3 install python-chess

import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from IterativeDeepeningAI import IterativeDeepeningAI
from QuiescenceAI import QuiescenceAI
from ImprovedAlphaBetaAI import ImprovedAlphaBetaAI
from EnhancedQAI import EnhancedQAI

from ChessGame import ChessGame

import sys

# for AlphaBetaAI and MinimaxAI, depth has to be specified as a parameter (e.g. MinimaxAI(depth=3))
player1 = MinimaxAI(depth=3)
player2 = EnhancedQAI(depth=3)

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()

print(game)  # Print the final board state
print(game.get_result())

# print(hash(str(game.board)))
