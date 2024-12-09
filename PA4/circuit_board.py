# Wesley Tan
# COSC 76 PA 4

from typing import List, Set, Dict, Tuple, Callable
import time
from csp import CSP, CSPSolver, create_generic_csp
import random

class Component:
    def __init__(self, name: str, width: int, height: int):
        self.name = name
        self.width = width
        self.height = height

class CircuitBoard:
    def __init__(self, width: int, height: int, components: List[Component]):
        if width <= 0 or height <= 0:
            raise ValueError("Board dimensions must be positive")
        if not components:
            raise ValueError("Must provide at least one component")
        for comp in components:
            if comp.width > width or comp.height > height:
                raise ValueError(f"Component {comp.name} is too large for the board")
            
        self.width = width
        self.height = height
        self.components = components
        self.solution = None
        
    def create_csp(self) -> CSP:
        """Creates and returns a CSP (Constraint Satisfaction Problem) representation of the circuit board layout problem.
        
        Returns:
            CSP: A CSP object where:
                - Variables are component names
                - Domains are valid (x,y) positions for each component
                - Constraints ensure no components overlap
        
        Raises:
            ValueError: If any component has no valid positions on the board
        """
        variables = [comp.name for comp in self.components]
        
        # Domain for each component is all possible positions on the board
        domains = {}
        for comp in self.components:
            positions = set()
            for x in range(self.width - comp.width + 1):
                for y in range(self.height - comp.height + 1):
                    # Add additional validation if needed
                    if x >= 0 and y >= 0 and x + comp.width <= self.width and y + comp.height <= self.height:
                        positions.add((x, y))
            if not positions:
                raise ValueError(f"No valid positions for component {comp.name}")
            domains[comp.name] = positions
        
        # Create non-overlapping constraints between all pairs of components
        constraints = []
        for i, comp1 in enumerate(self.components):
            for comp2 in self.components[i + 1:]:
                constraints.append((
                    comp1.name,
                    comp2.name,
                    lambda pos1, pos2, c1=comp1, c2=comp2: not self._components_overlap(
                        pos1, c1.width, c1.height,
                        pos2, c2.width, c2.height
                    )
                ))
        
        csp = CSP(len(variables), [domains[var] for var in variables])
        
        for var1, var2, constraint in constraints:
            allowed_pairs = []
            for val1 in domains[var1]:
                for val2 in domains[var2]:
                    if constraint(val1, val2):
                        allowed_pairs.append((val1, val2))
            csp.add_constraint(variables.index(var1), variables.index(var2), allowed_pairs)
        
        return csp
    
    def _components_overlap(self, pos1: Tuple[int, int], width1: int, height1: int,
                            pos2: Tuple[int, int], width2: int, height2: int) -> bool:
        """Determines if two components would overlap given their positions and dimensions.
        
        Args:
            pos1 (Tuple[int, int]): (x,y) position of first component
            width1 (int): Width of first component
            height1 (int): Height of first component
            pos2 (Tuple[int, int]): (x,y) position of second component
            width2 (int): Width of second component
            height2 (int): Height of second component
            
        Returns:
            bool: True if components overlap, False otherwise
        """
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Calculate the boundaries of each component
        left1, right1 = x1, x1 + width1
        top1, bottom1 = y1, y1 + height1
        left2, right2 = x2, x2 + width2
        top2, bottom2 = y2, y2 + height2
        
        # Check for overlap with a small tolerance for numerical precision
        return not (right1 <= left2 or  # 1 is left of 2
                   right2 <= left1 or  # 2 is left of 1
                   bottom1 <= top2 or  # 1 is below 2
                   bottom2 <= top1)    # 2 is below 1
    
    def solve(self, use_mrv=False, use_degree=False, use_lcv=False) -> bool:
        """Attempts to find a valid layout solution for the circuit board.
        
        Args:
            use_mrv (bool): Whether to use Minimum Remaining Values heuristic
            use_degree (bool): Whether to use Degree heuristic
            use_lcv (bool): Whether to use Least Constraining Value heuristic
            
        Returns:
            bool: True if a solution was found, False otherwise
            
        Side effects:
            - Sets self.solution to the solution if found, None otherwise
            - Prints solving time and number of nodes explored
        """
        csp = self.create_csp()
        solver = CSPSolver(csp, 
                         use_mrv=use_mrv,
                         use_degree=use_degree,
                         use_lcv=use_lcv)
        
        start_time = time.time()
        raw_solution = solver.backtrack()
        solve_time = time.time() - start_time
        
        self.solver = solver  # Store solver instance for statistics
        
        if raw_solution is not None:
            self.solution = {comp.name: raw_solution[i] for i, comp in enumerate(self.components)}
        else:
            self.solution = None

        print(f"\nSolution found in {solve_time:.4f} seconds")
        print(f"Nodes explored: {solver.nodes_explored}")
        
        return self.solution is not None
    
    def display_solution(self):
        """Displays the current board solution as ASCII art.
        
        The board is displayed with:
        - '.' for empty spaces
        - First letter of component name for occupied spaces
        - Border characters for the board edges
        
        If no solution exists, prints "No solution found!"
        """
        if not self.solution:
            print("No solution found!")
            return
            
        # Create empty board
        board = [['.'] * self.width for _ in range(self.height)]
        
        # Place components
        for comp in self.components:
            x, y = self.solution[comp.name]
            for i in range(comp.height):
                for j in range(comp.width):
                    board[y + i][x + j] = comp.name[0]
        
        # Print board
        print("\nCircuit Board Layout:")
        print("-" * (self.width + 2))
        for row in reversed(board):
            print("|" + "".join(row) + "|")
        print("-" * (self.width + 2))
    
    def display(self) -> str:
        """Returns a string representation of the current board solution.
        
        Returns:
            str: A string showing the board layout where:
                - '.' represents empty spaces
                - First letter of component name represents occupied spaces
                - Each row is separated by newlines
                Returns "No solution found!" if no solution exists
        """
        if not self.solution:
            return "No solution found!"
            
        # Create an empty board
        board_display = [['.'] * self.width for _ in range(self.height)]
        
        # Fill in placed components
        for comp in self.components:
            x, y = self.solution[comp.name]
            for i in range(comp.height):
                for j in range(comp.width):
                    board_display[y + i][x + j] = comp.name[0]
        
        # Convert to string
        return '\n'.join([''.join(row) for row in reversed(board_display)])

