# Wesley Tan
# COSC 76
# PA3: Chess AI

This project implements various Chess AI algorithms in Python using the python-chess library.

## Setup

1. Install Python 3.x
2. Install required packages:
   ```
   pip install python-chess
   ```

## Usage

The main entry point is `test_chess.py`, which demonstrates how to set up and run a game between two AI players.

### Running a Game

```python
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from ChessGame import ChessGame

# Create two AI players
player1 = RandomAI()
player2 = MinimaxAI(depth=2)

# Initialize and run the game
game = ChessGame(player1, player2)
while not game.is_game_over():
    print(game)
    game.make_move()

print(game)  # Print the final board state
print(game.get_result())
```

### Available AI Players

- `RandomAI()` - Makes random legal moves
- Q2. `MinimaxAI(depth=n)` - Uses minimax algorithm without iterative deepening
- Q3. `AlphaBetaAI(depth=n)` - Implements alpha-beta pruning
- Q4. `IterativeDeepeningAI(depth=n)` - Uses iterative deepening with minimax
- BONUS. `QuiescenceAI(depth=n)` - Adds advanced position evaluation
- BONUS. `ImprovedAlphaBetaAI(depth=n)` - Includes transposition tables and move ordering

The `depth` parameter controls how many moves ahead the AI will look. Higher values generally result in stronger play but require more computation time.
