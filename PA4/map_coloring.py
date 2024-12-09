# Wesley Tan
# COSC 76 PA 4

import time
from csp import CSP, CSPSolver
from typing import List, Dict, Tuple, Set, Optional, Callable

class MapColoringCSP(CSP):
    def __init__(self, regions: List[str], neighbors: List[Tuple[str, str]], colors: List[str]):
        # Create index mapping once
        self.region_index = {region: idx for idx, region in enumerate(regions)}
        self.colors = colors
        # Initialize domains as sets for more efficient operations
        domains = [{i for i in range(len(colors))} for _ in regions]
        super().__init__(len(regions), domains)
        
        # Pre-compute valid color pairs once
        color_pairs = [(i, j) for i in range(len(colors)) for j in range(len(colors)) if i != j]
        # Add constraints for neighboring regions
        for region1, region2 in neighbors:
            self.add_constraint(self.region_index[region1], self.region_index[region2], color_pairs)

    def solve(self, use_mrv=True, use_degree=True) -> Optional[Dict[str, str]]:
        """Solve the map coloring problem and return the solution"""
        solver = CSPSolver(self, use_mrv=use_mrv, use_degree=use_degree)
        solution = solver.backtrack()
        return self.convert_solution(solution) if solution else None

    def convert_solution(self, assignment: List[Optional[int]]) -> Dict[str, str]:
        """More concise solution conversion using dictionary comprehension"""
        return {region: self.colors[assignment[idx]] for region, idx in self.region_index.items()}


# def test_map_coloring_usa():
#     """
#     Test the USA map coloring with western states
#     Expected solution: Any valid 4-coloring where no adjacent states share colors
#     """
#     print("\n=== Test Case: Western USA Map ===")
#     print("Configuration: 11 states, 4 colors")
#     regions = ['WA', 'OR', 'CA', 'NV', 'ID', 'UT', 'AZ', 'MT', 'WY', 'CO', 'NM']
#     neighbors = [
#         ('WA', 'OR'), ('OR', 'CA'), ('OR', 'NV'), ('CA', 'NV'), ('NV', 'ID'),
#         ('NV', 'UT'), ('NV', 'AZ'), ('ID', 'MT'), ('ID', 'WY'), ('UT', 'CO'),
#         ('UT', 'AZ'), ('AZ', 'NM'), ('MT', 'WY'), ('WY', 'CO'), ('CO', 'NM')
#     ]
#     colors = ['red', 'purple', 'blue', 'yellow']
    
#     csp = MapColoringCSP(regions, neighbors, colors)
#     solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
#     solution = solver.backtrack()
#     if solution:
#         readable_solution = csp.convert_solution(solution)
#         print("\nSolution:")
#         for region, color in sorted(readable_solution.items()):
#             print(f"  {region}: {color}")
#         print(f"Performance: {solver.nodes_explored} nodes explored")
#     else:
#         print("Result: No solution found")

# test_map_coloring_usa()
