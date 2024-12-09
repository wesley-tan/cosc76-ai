The implementation uses a SAT (Boolean Satisfiability) solver to solve Sudoku puzzles by converting them to CNF (Conjunctive Normal Form) and applying two algorithms: WalkSAT and GSAT.
Implementation Details

Problem Representation


Variables are encoded as 3-digit numbers (rcv) where:

r: row (1-9)
c: column (1-9)
v: value (1-9)


Each variable represents whether a specific value is placed in a specific cell
The CNF formula includes clauses for:

Cell constraints (one value per cell)
Row/column/box uniqueness
Initial puzzle values




Key Optimizations


Variable-to-clause indexing using var_to_clauses for efficient clause lookup
Combined make/break calculation to reduce redundant evaluations
Early termination in GSAT when no improvements possible
Best solution tracking across all attempts
Solution validation to ensure Sudoku constraints


Algorithm Implementation

WalkSAT:

Random initial assignment with one value per cell
Probabilistic choice between:

Random walks (p = 0.3)
Greedy moves based on make-break scores


Progress tracking with best solution storage
Solution validation before acceptance

GSAT:

Similar initialization but with different strategy:

Random walks with probability h = 0.3
Complete neighborhood evaluation
Selection of best improvement


Earlier termination on plateaus

Evaluation
Effectiveness

Successful Solutions


Successfully solved standard 9x9 Sudoku puzzles
Example solution times:

Basic puzzle: Found in first try
Bonus puzzle: Found after ~20,000 flips
Both solutions validated correctly




Performance Characteristics


High initial satisfaction rate (96-97% of clauses)
Quick improvement to 99.9% satisfaction
WalkSAT showed better performance than GSAT:

Faster convergence
More reliable solutions
Better handling of local optima

Limitations and Considerations


Solution time varies with puzzle difficulty
Random initialization impacts convergence speed
Memory usage scales with problem size due to clause indexing
GSAT less effective due to complete neighborhood evaluation cost