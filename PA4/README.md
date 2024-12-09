# Wesley Tan
# COSC 76 PA 4

# CSP Solver Framework

This project implements a flexible Constraint Satisfaction Problem (CSP) solver framework with support for various classic problems and advanced heuristics.

## Features

- Generic CSP framework with support for:
  - Minimum Remaining Values (MRV) heuristic
  - Degree heuristic
  - Least Constraining Value (LCV) heuristic
  - AC-3 arc consistency algorithm

## Implemented Problems

### Map Coloring
- Classic map coloring problem implementation
- Supports arbitrary regions and color constraints
- Includes test cases for:
  - USA western states
  - Australia
  - Europe
  - Complete graphs
  - Edge cases (empty, single region)

### Circuit Board Layout
- Standard version with rectangular components
- BONUS version with:
  - Arbitrary component shapes
  - Non-rectangular components
  - Symmetry breaking optimization
  - Area-based validation

### N-Queens Problem
- Configurable board size
- Efficient constraint modeling
- Includes test cases for 4x4 and 8x8 boards

### BONUS: Sudoku Solver
- 9x9 grid implementation
- Box, row, and column constraints
- Performance metrics tracking

## Installation and Usage

Ensure you have Python 3.x installed. No additional dependencies required.

### Running the Problems

`csp.py` contains the generic CSP framework.
`map_coloring.py` contains the map coloring problem.
`circuit_board.py` contains the circuit board problem.
`test_map_coloring.py` contains the test cases for the map coloring problem.
`test_circuit_board.py` contains the test cases for the circuit board problem.

To run the test cases, use the following commands:

```
python test_map_coloring.py
python test_circuit_board.py
```

And the bonus problems:

```
python BONUS_circuit_board.py
python BONUS_nqueens.py
python BONUS_sudoku.py
```