# Wesley Tan
# COSC 76 PA 4

from csp import CSP, CSPSolver, create_generic_csp

# Sets up the n-queens problem as a CSP
def n_queens_csp(n: int) -> CSP:
    variables = [f"Q{i}" for i in range(n)]
    domains = {var: set(range(n)) for var in variables}

    def no_conflict(q1_row, q2_row, q1_col, q2_col):
        return q1_row != q2_row and abs(q1_row - q2_row) != abs(q1_col - q2_col) and q1_col != q2_col

    constraints = []
    for i in range(n):
        for j in range(i + 1, n):
            constraints.append((f"Q{i}", f"Q{j}", lambda r1, r2, i=i, j=j: no_conflict(r1, r2, i, j)))

    return create_generic_csp(variables, domains, constraints)

# Tests
print("4-Queens problem:")
n = 4  
csp = n_queens_csp(n)
solver = CSPSolver(csp)
solution = solver.backtrack()

if solution:
    print("Solution found:")
    board = [['.' for _ in range(n)] for _ in range(n)]
    for col, val in enumerate(solution):
        board[val][col] = 'Q'
    for row in board:
        print(' '.join(row))
else:
    print("No solution found.")

print("8-Queens problem:")
n = 8  # For 8-Queens problem
csp = n_queens_csp(n)
solver = CSPSolver(csp)
solution = solver.backtrack()

if solution:
    print("Solution found:")
    board = [['.' for _ in range(n)] for _ in range(n)]
    for col, val in enumerate(solution):
        board[val][col] = 'Q'
    for row in board:
        print(' '.join(row))
else:
    print("No solution found.")