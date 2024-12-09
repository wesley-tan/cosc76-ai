# N-Queens Problem Solver using SAT

from SAT import SAT
import sys

def generate_nqueens_cnf(n, filename):
    """Generate CNF file for N-Queens problem"""
    with open(filename, 'w') as f:
        # Each row must have exactly one queen
        for row in range(1, n+1):
            # At least one queen in each row
            positions = [str(row*100 + col) for col in range(1, n+1)]
            f.write(' '.join(positions) + '\n')
            
            # No two queens in same row
            for col1 in range(1, n+1):
                for col2 in range(col1+1, n+1):
                    f.write(f"-{row*100 + col1} -{row*100 + col2}\n")

        # Each column must have exactly one queen
        for col in range(1, n+1):
            # At least one queen in each column
            positions = [str(row*100 + col) for row in range(1, n+1)]
            f.write(' '.join(positions) + '\n')
            
            # No two queens in same column
            for row1 in range(1, n+1):
                for row2 in range(row1+1, n+1):
                    f.write(f"-{row1*100 + col} -{row2*100 + col}\n")

        # No queens on same diagonal
        for row1 in range(1, n+1):
            for col1 in range(1, n+1):
                # Check diagonals
                for offset in range(1, n):
                    # Down-right diagonal
                    if row1 + offset <= n and col1 + offset <= n:
                        f.write(f"-{row1*100 + col1} -{(row1+offset)*100 + (col1+offset)}\n")
                    # Down-left diagonal
                    if row1 + offset <= n and col1 - offset >= 1:
                        f.write(f"-{row1*100 + col1} -{(row1+offset)*100 + (col1-offset)}\n")

if __name__ == "__main__":
    N = 8  # Size of board
    cnf_file = "nqueens.cnf"
    sol_file = "nqueens.sol"

    # Generate CNF file
    generate_nqueens_cnf(N, cnf_file)

    # Solve using SAT solver
    sat = SAT(cnf_file)
    if sat.walksat():
        sat.write_solution(sol_file)
        print(f"\nSolution found for {N}-Queens problem!")
        
        # Display solution
        board = [['.'] * N for _ in range(N)]
        with open(sol_file, 'r') as f:
            for line in f:
                pos = int(line.strip())
                row = (pos // 100) - 1
                col = (pos % 100) - 1
                board[row][col] = 'Q'
        
        print("\nBoard configuration:")
        for row in board:
            print(' '.join(row))
    else:
        print(f"\nNo solution found for {N}-Queens problem.")