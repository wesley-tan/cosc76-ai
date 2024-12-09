from map_coloring import MapColoringCSP
from csp import CSPSolver

# Testing functions

def test_map_coloring_europe():
    """
    Test a simplified map of Western Europe
    Expected solution: Any valid 4-coloring where no adjacent countries share colors
    """
    print("\n=== Test Case: Western Europe Map ===")
    print("Configuration: 7 countries, 4 colors")
    regions = ['France', 'Germany', 'Italy', 'Spain', 'Portugal', 'Belgium', 'Netherlands']
    neighbors = [
        ('France', 'Germany'), ('France', 'Italy'), ('France', 'Spain'),
        ('Spain', 'Portugal'), ('Belgium', 'Netherlands'), ('Belgium', 'France'),
        ('Germany', 'Netherlands'), ('Germany', 'Belgium')
    ]
    colors = ['red', 'green', 'blue', 'purple']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    if solution:
        readable_solution = csp.convert_solution(solution)
        print("\nSolution:")
        for region, color in sorted(readable_solution.items()):
            print(f"  {region}: {color}")
        print(f"Performance: {solver.nodes_explored} nodes explored")
    else:
        print("Result: No solution found")

def test_map_coloring_small():
    """
    Test a small map with minimal regions
    Expected solution: Any valid coloring where no adjacent regions share colors
    Possible solution:
    A: red
    B: blue
    C: red
    """
    print("\n=== Test Case: Simple Linear Map ===")
    print("Configuration: 3 regions, 3 colors")
    regions = ['A', 'B', 'C']
    neighbors = [('A', 'B'), ('B', 'C')]
    colors = ['red', 'blue', 'green']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    if solution:
        readable_solution = csp.convert_solution(solution)
        print("\nSolution:")
        for region, color in sorted(readable_solution.items()):
            print(f"  {region}: {color}")
        print(f"Performance: {solver.nodes_explored} nodes explored")
    else:
        print("Result: No solution found")

def test_map_coloring_cycle():
    """
    Test a cyclic map arrangement
    Expected solution: Requires at least 3 colors
    Possible solution:
    A: red
    B: blue
    C: green
    D: red
    """
    print("\n=== Test Case: Cyclic Map ===")
    print("Configuration: 4 regions in a cycle, 3 colors")
    regions = ['A', 'B', 'C', 'D']
    neighbors = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]
    colors = ['red', 'blue', 'green']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    if solution:
        readable_solution = csp.convert_solution(solution)
        print("\nSolution:")
        for region, color in sorted(readable_solution.items()):
            print(f"  {region}: {color}")
        print(f"Performance: {solver.nodes_explored} nodes explored")
    else:
        print("Result: No solution found")

def test_map_coloring_complete():
    """
    Test a complete graph where every region is adjacent to every other region
    Expected solution: Requires exactly 4 colors (no solution with 3 colors)
    """
    print("\n=== Test Case: Complete Graph ===")
    print("Configuration: 4 regions, testing with 3 and 4 colors")
    regions = ['A', 'B', 'C', 'D']
    neighbors = [
        ('A', 'B'), ('A', 'C'), ('A', 'D'),
        ('B', 'C'), ('B', 'D'),
        ('C', 'D')
    ]
    
    # First try with 3 colors (should fail)
    colors_insufficient = ['red', 'blue', 'green']
    csp_insufficient = MapColoringCSP(regions, neighbors, colors_insufficient)
    solver_insufficient = CSPSolver(csp_insufficient, use_mrv=True, use_degree=True)
    
    print("\nPart 1: Testing complete graph with 3 colors (should fail):")
    solution = solver_insufficient.backtrack()
    if solution:
        print("Unexpected: Found solution with 3 colors!")
    else:
        print("As expected: No solution found with 3 colors")
    
    # Then try with 4 colors (should succeed)
    colors_sufficient = ['red', 'blue', 'green', 'yellow']
    csp_sufficient = MapColoringCSP(regions, neighbors, colors_sufficient)
    solver_sufficient = CSPSolver(csp_sufficient, use_mrv=True, use_degree=True)
    
    print("\nPart 2: Testing complete graph with 4 colors (should succeed):")
    solution = solver_sufficient.backtrack()
    if solution:
        readable_solution = csp_sufficient.convert_solution(solution)
        print("Complete Graph Solution found:")
        for region, color in sorted(readable_solution.items()):
            print(f"  {region}: {color}")
        print(f"Performance: {solver_sufficient.nodes_explored} nodes explored")
    else:
        print("Unexpected: No solution found with 4 colors")

def test_map_coloring_empty():
    """Test edge case: Empty map (should succeed trivially)"""
    print("\n=== Test Case: Empty Map (Edge Case) ===")
    regions = []
    neighbors = []
    colors = ['red']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    assert solution is not None, "Empty map should return a solution"
    assert isinstance(solution, dict), "Solution should be a dictionary"
    assert len(solution) == 0, "Empty map should return empty solution"
    print("Result: Test passed")

def test_map_coloring_single():
    """Test edge case: Single region (should succeed with one color)"""
    print("\n=== Test Case: Single Region Map (Edge Case) ===")
    regions = ['A']
    neighbors = []
    colors = ['red']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    assert solution is not None, "Single region should be solvable"
    print("Result: Test passed")

def test_map_coloring_insufficient_colors():
    """Test edge case: Not enough colors for the constraints"""
    print("\n=== Test Case: Triangle Map with Insufficient Colors ===")
    print("Configuration: 3 regions, 2 colors (should fail)")
    regions = ['A', 'B', 'C']
    neighbors = [('A', 'B'), ('B', 'C'), ('C', 'A')]  # Triangle needs 3 colors
    colors = ['red', 'blue']  # Only 2 colors provided
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    assert solution is None, "Should not find solution with insufficient colors"
    print("Result: Test passed (no solution as expected)")

def test_map_coloring_disconnected():
    """Test case: Disconnected regions (multiple components)"""
    print("\n=== Test Case: Disconnected Map (Two components with 3 regions each) ===")
    regions = ['A', 'B', 'C', 'D', 'E', 'F']
    neighbors = [
        ('A', 'B'), ('B', 'C'),  # Component 1
        ('D', 'E'), ('E', 'F')   # Component 2
    ]
    colors = ['red', 'blue']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    assert solution is not None, "Disconnected regions should be solvable with 2 colors"
    print("Result: Test passed")

def test_map_coloring_australia():
    """
    Test the classic Australia map coloring problem
    Known to be solvable with 3 colors
    """
    print("\n=== Test Case: Australia Map Coloring ===")
    print("Configuration: 7 regions, 3 colors")
    regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    neighbors = [
        ('WA', 'NT'), ('WA', 'SA'), ('NT', 'SA'), ('NT', 'Q'),
        ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('Q', 'NSW'),
        ('NSW', 'V')
        # Tasmania (T) is disconnected from mainland
    ]
    colors = ['red', 'green', 'blue']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    assert solution is not None, "Australia should be 3-colorable"
    print("Result: Test passed")

def test_map_coloring_with_configurations(test_name, regions, neighbors, colors):
    """
    Test map coloring with different solver configurations and compare performance
    """
    print(f"\n=== {test_name} ===")
    print(f"Regions: {len(regions)}, Colors: {len(colors)}")
    
    # Test configurations
    configs = [
        ("Basic (No heuristics/inference)", False, False, False, False),
        ("MRV only", True, False, False, False),
        ("MRV + Degree", True, True, False, False),
        ("MRV + Degree + LCV", True, True, True, False),
        ("MRV + Degree + AC3", True, True, False, True),
        ("All heuristics + AC3", True, True, True, True)
    ]
    
    results = []
    for name, use_mrv, use_degree, use_lcv, use_ac3 in configs:
        csp = MapColoringCSP(regions, neighbors, colors)
        solver = CSPSolver(csp, use_mrv=use_mrv, use_degree=use_degree, 
                         use_lcv=use_lcv, use_ac3=use_ac3)
        
        solution = solver.backtrack()
        results.append({
            'config': name,
            'solved': solution is not None,
            'nodes': solver.nodes_explored
        })
        
    # Print results table
    print("\nResults:")
    print(f"{'Configuration':<25} {'Solved':<10} {'Nodes Explored':<15}")
    print("-" * 50)
    for result in results:
        print(f"{result['config']:<25} {str(result['solved']):<10} {result['nodes']:<15}")

def test_map_coloring_usa():
    """
    Test a simplified map of the United States
    Expected solution: Any valid 4-coloring where no adjacent states share colors
    """
    print("\n=== Test Case: United States Map ===")
    print("Configuration: 11 states, 4 colors")
    regions = ['CA', 'NV', 'OR', 'WA', 'ID', 'AZ', 'UT', 'NM', 'CO', 'WY', 'MT']
    neighbors = [
        ('CA', 'OR'), ('CA', 'NV'), ('CA', 'AZ'),
        ('OR', 'WA'), ('OR', 'ID'), ('OR', 'NV'),
        ('WA', 'ID'),
        ('ID', 'MT'), ('ID', 'WY'), ('ID', 'UT'), ('ID', 'NV'),
        ('NV', 'UT'), ('NV', 'AZ'),
        ('AZ', 'NM'), ('AZ', 'UT'),
        ('UT', 'WY'), ('UT', 'CO'), ('UT', 'NM'),
        ('NM', 'CO'),
        ('CO', 'WY'),
        ('WY', 'MT')
    ]
    colors = ['red', 'green', 'blue', 'yellow']
    
    csp = MapColoringCSP(regions, neighbors, colors)
    solver = CSPSolver(csp, use_mrv=True, use_degree=True)
    
    solution = solver.backtrack()
    if solution:
        readable_solution = csp.convert_solution(solution)
        print("\nSolution:")
        for region, color in sorted(readable_solution.items()):
            print(f"  {region}: {color}")
        print(f"Performance: {solver.nodes_explored} nodes explored")
    else:
        print("Result: No solution found")

# Add the new test calls to main
if __name__ == "__main__":
    print("=== Map Coloring CSP Test Suite ===")
    
    print("\nRunning Edge Cases:")
    test_map_coloring_empty()
    test_map_coloring_single()
    test_map_coloring_insufficient_colors()
    
    print("\nRunning Basic Tests:")
    test_map_coloring_small()
    test_map_coloring_cycle()
    test_map_coloring_disconnected()
    
    print("\nRunning Complex Tests:")
    test_map_coloring_complete()
    test_map_coloring_australia()
    test_map_coloring_europe()
    test_map_coloring_usa()
    
    # Test with Australia map
    australia_regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    australia_neighbors = [
        ('WA', 'NT'), ('WA', 'SA'), ('NT', 'SA'), ('NT', 'Q'),
        ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('Q', 'NSW'),
        ('NSW', 'V')
    ]
    australia_colors = ['red', 'green', 'blue']
    
    test_map_coloring_with_configurations(
        "Australia Map Performance Comparison",
        australia_regions,
        australia_neighbors,
        australia_colors
    )
    
    # Test with Europe map (more complex)
    europe_regions = ['France', 'Germany', 'Italy', 'Spain', 'Portugal', 
                     'Belgium', 'Netherlands']
    europe_neighbors = [
        ('France', 'Germany'), ('France', 'Italy'), ('France', 'Spain'),
        ('Spain', 'Portugal'), ('Belgium', 'Netherlands'), ('Belgium', 'France'),
        ('Germany', 'Netherlands'), ('Germany', 'Belgium')
    ]
    europe_colors = ['red', 'green', 'blue', 'purple']
    
    test_map_coloring_with_configurations(
        "Europe Map Performance Comparison",
        europe_regions,
        europe_neighbors,
        europe_colors
    )
    
    # Add USA map performance comparison
    usa_regions = ['CA', 'NV', 'OR', 'WA', 'ID', 'AZ', 'UT', 'NM', 'CO', 'WY', 'MT']
    usa_neighbors = [
        ('CA', 'OR'), ('CA', 'NV'), ('CA', 'AZ'),
        ('OR', 'WA'), ('OR', 'ID'), ('OR', 'NV'),
        ('WA', 'ID'),
        ('ID', 'MT'), ('ID', 'WY'), ('ID', 'UT'), ('ID', 'NV'),
        ('NV', 'UT'), ('NV', 'AZ'),
        ('AZ', 'NM'), ('AZ', 'UT'),
        ('UT', 'WY'), ('UT', 'CO'), ('UT', 'NM'),
        ('NM', 'CO'),
        ('CO', 'WY'),
        ('WY', 'MT')
    ]
    usa_colors = ['red', 'green', 'blue', 'yellow']
    
    test_map_coloring_with_configurations(
        "USA Map Performance Comparison",
        usa_regions,
        usa_neighbors,
        usa_colors
    )
