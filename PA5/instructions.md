Skip to content
0/7 Questions Answered
PA5 - Logic
Q1 The problem
10 Points
Grading comment:
Your goal for this assignment is to write a few solvers for propositional logic satisfiability problems. As an example, we'll use sets of sentences derived from sudoku logic puzzles. The learning objective is to model and solve propositional logic satisfiability problems, discussed in class. 

==Getting started==
Here are some provided data and code to get you started. The most important provided files end with the extension .cnf. These are representations of the problems you will solve, in conjunctive normal form.

There are also Python files. Sudoku.py is the workhorse: it converts .sud data files to conjunctive normal form and can be used to display text representations of boards. sudoku2cnf.py is a utility that lets you quickly do the conversion from the command-line. display.py will display a *.sol solution file, described later.

solve_sudoku.py solves and displays a .cnf sudoku problem. Well, it would, if there were a "SAT.py" file containing a boolean satisfiability solver. Your main job will be to write that solver.

You don't have to use any of the provided code unless you want to. The provided Sudoku problems are already in .cnf format, and the display and loading code is quite trivial; you could write your own in a few minutes if you prefer to.
The format of the cnf files is based loosely on that described by Ivor Spence here. 

More details about cnf and implementation are reported below in Q2.

==Required tasks==
1. Implement GSAT
The GSAT algorithm intuition is described on Wikipedia. It is quite simple. The pseudocode can be found at the related research paper.

1) Choose a random assignment (a model).
2) If the assignment satisfies all the clauses, stop.
3) Pick a number between 0 and 1. If the number is greater than some threshold h, choose a variable uniformly at random and flip it; go back to step 2.
3) Otherwise, for each variable, score how many clauses would be satisfied if the variable value were flipped.
4) Uniformly at random choose one of the variables with the highest score. (There may be many tied variables.) Flip that variable. Go back to step 2.

Implement GSAT (see implementation notes below before starting). You should be able to solve the first few .cnf problems with your implementation. The real sudoku puzzles are probably too hard to solve with GSAT in a reasonable time frame, however.

2. Implement WalkSAT
The scoring step in GSAT can be slow. If there are 729 variables, and a few thousand clauses, the obvious scoring method (and I haven't clearly thought out a better one) loops more than a million times. And that only flips a single bit in the assignment. Ouch.

WalkSAT chooses a smaller number of candidate variables that might be flipped. For the current assignment, some clauses are unsatisfied. Choose one of these unsatisfied clauses uniformly at random. The resulting set will be your candidate set. Use these candidate variables when scoring. Implement WalkSAT.

I found that WalkSAT needed very many iterations to solve puzzle1.cnf and puzzle2.cnf. I limited to 100,000 iterations, and chose .3 as my magic threshold value for a random move in step 3.

There are many variations on WalkSAT. Some variations do a GSAT step occasionally to try to escape local minima. You should implement the simple version described above as a first step, although exploration of variants is always welcome as an extension.

3. Write-up
Write: 

a report to discuss your implementation, which contains the following information:
a. Header with the code of the class, the term, and year, the assignment number, and your name.
b. A short typewritten report describing your results. The report should contain two sections (there are no explicit discussion questions for this PA):
  (a) Description: How do your implemented algorithms work? What design decisions did you make? How you laid out the problems?
  (b) Evaluation: Do your implemented algorithms actually work? How well? If it doesn’t work, can you tell why not? What partial successes did you have that deserve partial credit? 
a README file with the instructions on how to execute the program.
Question 1.1 Rubric and grading
Q1.1 Rubric and grading
0 Points
Grading comment:
Your code should be efficient and well-designed, with excellent style, formatting, comments. It should be brief if possible.

WalkSAT: 3
GSAT: 3
General code quality: 1.5
Report: 2.5
Bonus as specified in the syllabus (see below for ideas of extensions.)
Submit your .md, .pdf, and Python source files, bundled into a single zip.  Please also include a very short README file that explains how to run your code. If there is any comment you want to add attached to the submission, please use the text box.

No file chosenPlease select file(s)Select file(s)
Save Answer
Question 1.1: Rubric and grading
Question 1.2 WalkSAT (placeholder for grade)
Q1.2 WalkSAT (placeholder for grade)
3 Points
Grading comment:
Save Answer
Question 1.2: WalkSAT (placeholder for grade)
Question 1.3 GSAT (placeholder for grade)
Q1.3 GSAT (placeholder for grade)
3 Points
Grading comment:
Save Answer
Question 1.3: GSAT (placeholder for grade)
Question 1.4 General code quality (placeholder for grade)
Q1.4 General code quality (placeholder for grade)
1.5 Points
Grading comment:
Save Answer
Question 1.4: General code quality (placeholder for grade)
Question 1.5 Report (placeholder for grade)
Q1.5 Report (placeholder for grade)
2.5 Points
Grading comment:
Save Answer
Question 1.5: Report (placeholder for grade)
Q2 Details
0 Points
Grading comment:
CNF details
Each line of a .cnf file represents a or-clause in cnf. Thus, the line

111 112 113 114 115 116 117 118 119
indicates that at least one of the variables 111, 112, 113, etc, must have the value True. Negative signs indicate negation. The line

-111 -112
indicates that either 111 or 112 must have the value False. Since this is conjunctive normal form, every clause must be satisfied to solve the problem, but there are multiple variables in most clauses, and thus multiple ways to satisfy each clause.

The variable names correspond to locations and values on the sudoku board. 132 indicates that row 1, column 3 has a 2 in it. For a typical 9x9 sudoku board, there are therefore 729 variables.

The cnf files
In order of increasing difficulty, the files are:

one_cell.cnf: rules that ensure that the upper left cell has exactly one value between 1 and 9.
all_cells.cnf: rules that ensure that all cells have exactly one value between 1 and 9.
rows.cnf: rules that ensure that all cells have a value, and every row has nine unique values.
rows_and_cols.cnf: rules that ensure that all cells have a value, every row has nine unique values, and every column has nine unique values.
rules.cnf: adds block constraints, so each block has nine unique values. (The complete rules for an empty sudoku board.)
puzzle1.cnf: Adds a few starting values to the game to make a puzzle.
puzzle2.cnf: Some different starting values.
puzzle_bonus.cnf: Several starting values. Difficult; solution welcome but not required.
Implementation details
The variable names for Sudoku are things like 111, 234, etc. But your SAT-solvers should be generic -- they should accept any CNF problem, not just Sudoku problems. So you might expect variable names like VICTORIA_BLUE for a map coloring problem, or MINE_32 for minesweeper. Thus, your code should probably refer to variables by numerical indices during calculation. Perhaps 111 is variable 1, and 112 is variable 2, etc. Then your assignment can be represented using a simple list. Clauses can also be converted into lists, or perhaps sets, of integers.

Representing variables and clauses in code
In a clause, I used a negative integer to represent a negated atomic variable. So the clause -1, -2 might represent -111 or -112. In my first implementation, this clever trick got me in trouble, because I decided that 111 was variable 0. Unfortunately, since -0 is the same as +0, some of the clauses involving the 0th variable got mangled -- a tricky bug to find. So don't 0-index your variables! This also has implications for assignments. If the assignment is a list, then index 0 might refer to the value of variable 1. So be careful with your indexing, too.

Output .sol files
It's wise to output a solution file when you run the solver, since the solver might take several minutes for a hard problem. I output files with '.sol' extensions that listed the name of every variable in the assignment, with either no sign (for a true value), or a negative sign (for a false value). I put each variable name on its own line in the file.

Notice that this is perhaps redundant, since knowing which variables are true tells you that the others are false. I did it anyway, since that way I get a complete list of the variable names, and disk space is cheap.

Save Answer
Question 2: Details
Q3 Possible extensions for bonus credit (optional)
0 Points
Grading comment:
As usual, any scientifically interesting extension related to the theme of the assignment is welcome. Here are a few ideas to get you started, but you need not limit yourself to these ideas.

1) Resolution. Implement a resolution solver and prove some things. For example, you might set up a small sudoku problem (just the upper left block, perhaps), and initialize it with some values. Then try to prove something about some of the other values. I believe that most humans do this when trying to solve Sudoku. I know I use a combination of proofs of this form, and random walks.

2) Solve some other satisfiability problems. Map-coloring is obvious and easy. Can you find others?

3) Solve some interesting resolution problem(s). Perhaps minesweeper. In your report, describe the problem set-up. You might wish to constrain the problem to a small piece of the board.

4) Implement a deterministic solver for satisfiability, such as DPLL. Compare to WalkSAT.

5) Implement another random walk algorithm (perhaps one more sophisticated than walksat). Compare.

6) WalkSAT violates constraints at every step, including known cell values. Is the fact that the solver ignores the fact that some variables have known values a good thing? A bad thing? Make arguments for both, and do some experimental work by modifying the cnf to eliminate the known variables, and then running walksat. (That is, if 342 is known to be true, it is a constant, not a variable, and might be treated as such.)

7) Ivor Spence's formulation adds several redundant constraints, as discussed on the linked page. Ivor argues that these constraints speed up the solver. My formulations do not include these constraints. Is your solver also faster if you add these constraints? Try it and report your results.

Save Answer
Question 3: Possible extensions for bonus credit (optional)
Save All Answers
Submit & View Submission 
