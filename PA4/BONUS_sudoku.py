from typing import List, Set, Optional
from csp import CSP, CSPSolver
import time

class SudokuCSP:
    def __init__(self, board: List[List[int]]):
        """Initialize Sudoku puzzle with a 9x9 board where 0 represents empty cells"""
        self.board = board
        self.size = 9
        self.box_size = 3
        
    def create_csp(self) -> CSP:
        """Convert Sudoku puzzle to CSP"""
        # Create variables (81 cells)
        num_variables = self.size * self.size
        
        # Domain for each variable is 1-9, unless already filled
        domains = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    domains.append(set(range(1, 10)))
                else:
                    domains.append({self.board[i][j]})
        
        # Create CSP instance
        csp = CSP(num_variables, domains)
        
        # Add constraints
        for row in range(self.size):
            for i in range(self.size):
                for j in range(i + 1, self.size):
                    var1 = row * self.size + i
                    var2 = row * self.size + j
                    self._add_inequality_constraint(csp, var1, var2)
        
        for col in range(self.size):
            for i in range(self.size):
                for j in range(i + 1, self.size):
                    var1 = i * self.size + col
                    var2 = j * self.size + col
                    self._add_inequality_constraint(csp, var1, var2)
        
        # 3x3 box constraints
        for box_row in range(self.box_size):
            for box_col in range(self.box_size):
                cells = self._get_box_cells(box_row, box_col)
                for i in range(len(cells)):
                    for j in range(i + 1, len(cells)):
                        self._add_inequality_constraint(csp, cells[i], cells[j])
        
        return csp
    
    def _add_inequality_constraint(self, csp: CSP, var1: int, var2: int):
        """Add constraint that two variables must have different values"""
        allowed_pairs = []
        for val1 in range(1, 10):
            for val2 in range(1, 10):
                if val1 != val2:
                    allowed_pairs.append((val1, val2))
        csp.add_constraint(var1, var2, allowed_pairs)
    
    def _get_box_cells(self, box_row: int, box_col: int) -> List[int]:
        """Get variable indices for cells in a 3x3 box"""
        cells = []
        start_row = box_row * self.box_size
        start_col = box_col * self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                cell_idx = (start_row + i) * self.size + (start_col + j)
                cells.append(cell_idx)
        return cells
    
    def solve(self) -> Optional[List[List[int]]]:
        """Solve the Sudoku puzzle and return solution with performance metrics"""
        start_time = time.time()
        csp = self.create_csp()
        solver = CSPSolver(csp, use_mrv=True, use_degree=True, use_lcv=True)
        solution = solver.backtrack()
        solve_time = time.time() - start_time
        
        if solution:
            # Convert solution back to 9x9 grid
            result = [[0] * self.size for _ in range(self.size)]
            for i in range(self.size):
                for j in range(self.size):
                    result[i][j] = solution[i * self.size + j]
            print(f"\nPerformance Metrics:")
            print(f"Solve time: {solve_time:.3f} seconds")
            print(f"Nodes explored: {solver.nodes_explored}")
            return result
        return None

def display_board(board: List[List[int]]):
    """Display Sudoku board in a readable format"""
    print("\n")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j], end=" ")
        print()

# Test the Sudoku solver
if __name__ == "__main__":
    # Test cases with varying difficulty
    test_cases = {
        "Easy": [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ],
        "Hard": [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ]
    }

    # Test each puzzle
    for difficulty, board in test_cases.items():
        print(f"\n{'-'*40}")
        print(f"Testing {difficulty} puzzle:")
        print(f"{'-'*40}")
        
        print("Original puzzle:")
        display_board(board)
        
        start_time = time.time()
        sudoku = SudokuCSP(board)
        solution = sudoku.solve()
        total_time = time.time() - start_time
        
        if solution:
            print("\nSolution found:")
            display_board(solution)
            print(f"Total execution time: {total_time:.3f} seconds")
        else:
            print("\nNo solution exists!")
