from typing import List, Set, Dict, Tuple, Callable
import time
from csp import CSP, CSPSolver, create_generic_csp
import random

"""
BONUS: Circuit Board
Adds:
- Arbitrary component shapes
- Symmetry breaking
- Non-rectangular component support
"""

class Component:
    def __init__(self, name: str, shape_matrix: List[List[bool]]):
        """
        Initialize component with name and shape matrix
        shape_matrix: 2D list of booleans where True indicates presence of component
        """
        self.name = name
        self.shape_matrix = shape_matrix
        self.height = len(shape_matrix)
        self.width = len(shape_matrix[0]) if self.height > 0 else 0
        
        # Validate shape matrix
        if not all(len(row) == self.width for row in shape_matrix):
            raise ValueError(f"Component {name} has inconsistent row lengths")
        if not any(any(row) for row in shape_matrix):
            raise ValueError(f"Component {name} has no active cells")
            
    def __repr__(self):
        return f"Component({self.name}, {self.width}x{self.height})"
        
    def display_shape(self):
        """Display the component's shape"""
        print(f"\nComponent {self.name} shape:")
        for row in self.shape_matrix:
            print("".join('#' if cell else '.' for cell in row))

class CircuitBoard:
    def __init__(self, width: int, height: int, components: List[Component]):
        self.width = width
        self.height = height
        self.components = components
        self.solution = None
        self.use_symmetry_breaking = True
        self.use_mrv = True
        self.use_degree = True
        self.use_lcv = True
        self.use_ac3 = True
        
    def create_csp(self) -> CSP:
        variables = [comp.name for comp in self.components]
        
        # Calculate total area and component areas
        total_board_area = self.width * self.height
        component_areas = {comp.name: sum(sum(row) for row in comp.shape_matrix) 
                         for comp in self.components}
        total_component_area = sum(component_areas.values())
        
        print(f"\nBoard area: {total_board_area}")
        print(f"Total component area: {total_component_area}")
        for comp in self.components:
            print(f"Component {comp.name} area: {component_areas[comp.name]}")
            comp.display_shape()
        
        if total_component_area > total_board_area:
            print("Warning: Components require more area than available on board")
        
        # Generate domains
        domains = {}
        for comp in self.components:
            positions = set()
            for x in range(self.width - comp.width + 1):
                for y in range(self.height - comp.height + 1):
                    # Check if position is valid considering component shape
                    if self._is_valid_position(x, y, comp.shape_matrix):
                        positions.add((x, y))
            domains[comp.name] = positions
            print(f"Component {comp.name} has {len(positions)} possible positions")
        
        # Generate constraints
        constraints = []
        for i, comp1 in enumerate(self.components):
            for comp2 in self.components[i + 1:]:
                constraints.append((
                    comp1.name,
                    comp2.name,
                    lambda pos1, pos2, c1=comp1, c2=comp2: not self._components_overlap(
                        pos1, c1.shape_matrix,
                        pos2, c2.shape_matrix
                    )
                ))
        
        # Add symmetry breaking for identical components
        if self.use_symmetry_breaking:
            for i in range(len(self.components)-1):
                comp1 = self.components[i]
                comp2 = self.components[i+1]
                if (comp1.width == comp2.width and 
                    comp1.height == comp2.height and 
                    comp1.shape_matrix == comp2.shape_matrix):
                    constraints.append((
                        comp1.name,
                        comp2.name,
                        lambda pos1, pos2: pos1 < pos2
                    ))
        
        # Create and return CSP
        csp = CSP(len(variables), [domains[var] for var in variables])
        
        for var1, var2, constraint in constraints:
            allowed_pairs = []
            for val1 in domains[var1]:
                for val2 in domains[var2]:
                    if constraint(val1, val2):
                        allowed_pairs.append((val1, val2))
            csp.add_constraint(variables.index(var1), variables.index(var2), allowed_pairs)
        
        return csp
    
    def _is_valid_position(self, x: int, y: int, shape_matrix: List[List[bool]]) -> bool:
        """Check if a component's position is valid on the board"""
        height = len(shape_matrix)
        width = len(shape_matrix[0])
        
        # Check if any active cell would be off the board
        for i in range(height):
            for j in range(width):
                if shape_matrix[i][j]:
                    board_x = x + j
                    board_y = y + i
                    if (board_x < 0 or board_x >= self.width or
                        board_y < 0 or board_y >= self.height):
                        return False
        return True
    
    def _components_overlap(self, pos1: Tuple[int, int], shape1: List[List[bool]],
                          pos2: Tuple[int, int], shape2: List[List[bool]]) -> bool:
        """Check if two components with arbitrary shapes overlap"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Check each active cell of first component against each active cell of second
        for i1 in range(len(shape1)):
            for j1 in range(len(shape1[0])):
                if not shape1[i1][j1]:
                    continue
                board_x1 = x1 + j1
                board_y1 = y1 + i1
                
                for i2 in range(len(shape2)):
                    for j2 in range(len(shape2[0])):
                        if not shape2[i2][j2]:
                            continue
                        board_x2 = x2 + j2
                        board_y2 = y2 + i2
                        
                        if board_x1 == board_x2 and board_y1 == board_y2:
                            return True
        return False
    
    def solve(self) -> bool:
        """Solve the circuit board layout problem"""
        csp = self.create_csp()
        solver = CSPSolver(csp, 
                         use_mrv=self.use_mrv,
                         use_degree=self.use_degree,
                         use_lcv=self.use_lcv,
                         use_ac3=self.use_ac3)
        
        start_time = time.time()
        raw_solution = solver.backtrack()
        solve_time = time.time() - start_time
        
        if raw_solution is not None:
            self.solution = {comp.name: raw_solution[i] for i, comp in enumerate(self.components)}
            print(f"\nSolution found in {solve_time:.4f} seconds")
            print(f"Nodes explored: {solver.nodes_explored}")
            return True
        else:
            self.solution = None
            print(f"\nNo solution found after {solve_time:.4f} seconds")
            print(f"Nodes explored: {solver.nodes_explored}")
            return False
    
    def display_solution(self):
        """Display the circuit board layout as ASCII art"""
        if not self.solution:
            print("No solution found!")
            return
            
        # Create empty board
        board = [['.'] * self.width for _ in range(self.height)]
        
        # Place components
        for comp in self.components:
            x, y = self.solution[comp.name]
            for i in range(len(comp.shape_matrix)):
                for j in range(len(comp.shape_matrix[0])):
                    if comp.shape_matrix[i][j]:
                        board[y + i][x + j] = comp.name[0]
        
        # Print board
        print("\nCircuit Board Layout:")
        print("-" * (self.width + 2))
        for row in reversed(board):
            print("|" + "".join(row) + "|")
        print("-" * (self.width + 2))
        
def test_shapes():
    """Test various component shapes"""
    tests = [
        # Test 1: Basic shapes
        {
            "name": "Basic Shapes",
            "board": (4, 4),
            "components": [
                Component("L", [[True, False],
                              [True, True]]),
                Component("T", [[True, True, True],
                              [False, True, False]]),
            ]
        },
        
        # Test 2: Perfect fit
        {
            "name": "Perfect Fit",
            "board": (4, 4),
            "components": [
                Component("A", [[True, True],
                              [True, True]]) for _ in range(4)
            ]
        },
        
        # Test 3: Complex shapes
        {
            "name": "Complex Shapes",
            "board": (5, 5),
            "components": [
                Component("Z", [[True, True, False],
                              [False, True, True]]),
                Component("U", [[True, False, True],
                              [True, True, True]]),
            ]
        },
        
        # Test 4: Mixed shapes
        {
            "name": "Mixed Shapes",
            "board": (6, 4),
            "components": [
                Component("S", [[True, True],
                              [True, False]]),
                Component("L", [[True, False],
                              [True, False],
                              [True, True]]),
                Component("I", [[True],
                              [True],
                              [True]]),
            ]
        },
        
        # Additional Perfect Fit Tests
        {
            "name": "Perfect Fit - Vertical Strips",
            "board": (4, 4),
            "components": [
                Component("A", [[True], [True], [True], [True]]),
                Component("B", [[True], [True], [True], [True]]),
                Component("C", [[True], [True], [True], [True]]),
                Component("D", [[True], [True], [True], [True]])
            ]
        },
        {
            "name": "Perfect Fit - Mixed Tetris",
            "board": (4, 4),
            "components": [
                Component("L", [[True, False],
                              [True, False],
                              [True, True]]),
                Component("I", [[True],
                              [True],
                              [True],
                              [True]]),
                Component("S", [[False, True, True],
                              [True, True, False]])
            ]
        },
        {
            "name": "Perfect Fit - Exact Cover",
            "board": (3, 3),
            "components": [
                Component("A", [[True, True],
                              [True, False]]),
                Component("B", [[True],
                              [True],
                              [True]]),
                Component("C", [[False, True],
                              [True, True]])
            ]
        }
    ]
    
    # Test each case with and without symmetry breaking
    for test in tests:
        print(f"\n=== Testing {test['name']} ===")
        
        # Test with symmetry breaking
        print("With symmetry breaking:")
        board = CircuitBoard(test['board'][0], test['board'][1], test['components'])
        board.use_symmetry_breaking = True
        if board.solve():
            board.display_solution()
        else:
            print("No solution found!")
            
        # Test without symmetry breaking
        print("\nWithout symmetry breaking:")
        board = CircuitBoard(test['board'][0], test['board'][1], test['components'])
        board.use_symmetry_breaking = False
        if board.solve():
            board.display_solution()
        else:
            print("No solution found!")
            
    # Example of testing with different heuristic combinations
    test = tests[0]  # Use first test case
    print(f"\n=== Testing {test['name']} with different heuristics ===")
    
    heuristic_combinations = [
        {"name": "All heuristics + AC-3", "mrv": True, "degree": True, "lcv": True, "ac3": True},
        {"name": "All heuristics without AC-3", "mrv": True, "degree": True, "lcv": True, "ac3": False},
        {"name": "Only AC-3", "mrv": False, "degree": False, "lcv": False, "ac3": True},
        {"name": "No heuristics", "mrv": False, "degree": False, "lcv": False, "ac3": False},
        {"name": "MRV + AC-3", "mrv": True, "degree": False, "lcv": False, "ac3": True},
        {"name": "Degree + AC-3", "mrv": False, "degree": True, "lcv": False, "ac3": True},
        {"name": "LCV + AC-3", "mrv": False, "degree": False, "lcv": True, "ac3": True},
    ]
    
    for config in heuristic_combinations:
        print(f"\n--- {config['name']} ---")
        board = CircuitBoard(test['board'][0], test['board'][1], test['components'])
        board.use_mrv = config['mrv']
        board.use_degree = config['degree']
        board.use_lcv = config['lcv']
        board.use_ac3 = config['ac3']
        if board.solve():
            board.display_solution()
        else:
            print("No solution found!")

if __name__ == "__main__":
    test_shapes()