# Sudoku SAT Solver

This program implements a SAT solver to solve Sudoku puzzles by converting them to CNF and using WalkSAT algorithm.

## Prerequisites

- Python 3.x

## File Structure

- `Sudoku.py` - Main class for Sudoku board representation and CNF conversion
- `sudoku2cnf.py` - Utility to convert .sud files to CNF format
- `solve_sudoku.py` - Main solver that uses WalkSAT to solve the puzzle
- `display.py` - Utility to display solved Sudoku puzzles
- `SAT.py` - Implementation of the SAT solver (WalkSAT algorithm)

## Usage

1. To convert a Sudoku puzzle (.sud file) to CNF format:
```
python sudoku2cnf.py puzzle1.sud
```

2. To solve a Sudoku puzzle:
```
python solve_sudoku.py puzzle1.cnf
```
Replace `puzzle1.cnf` with the name of your Sudoku puzzle file.