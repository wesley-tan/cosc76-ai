from circuit_board import CircuitBoard, Component
import time

def test_basic_layout():
    """Test basic rectangular components layout"""
    print("\n=== Test Case: Basic Layout ===")
    components = [
        Component("A", 2, 2),  # 2x2 square
        Component("B", 2, 1),  # 2x1 rectangle
        Component("C", 1, 2)   # 1x2 rectangle
    ]
    board = CircuitBoard(4, 4, components)
    if board.solve():
        board.display_solution()
    else:
        print("No solution found!")

def test_perfect_fit():
    """Test case where components exactly fill the board"""
    print("\n=== Test Case: Perfect Fit ===")
    components = [
        Component("A", 2, 2),
        Component("B", 2, 2),
        Component("C", 2, 2),
        Component("D", 2, 2)
    ]
    board = CircuitBoard(4, 4, components)
    if board.solve():
        board.display_solution()
    else:
        print("No solution found!")

def test_impossible_fit():
    """Test case where components cannot fit on the board"""
    print("\n=== Test Case: Impossible Fit ===")
    components = [
        Component("A", 3, 3),
        Component("B", 3, 3)
    ]
    board = CircuitBoard(4, 4, components)
    if board.solve():
        board.display_solution()
    else:
        print("No solution found!")

def test_single_component():
    """Test case with a single component"""
    print("\n=== Test Case: Single Component ===")
    components = [Component("A", 2, 3)]
    board = CircuitBoard(3, 4, components)
    if board.solve():
        board.display_solution()
    else:
        print("No solution found!")

def test_linear_arrangement():
    """Test case with components that must be arranged linearly"""
    print("\n=== Test Case: Linear Arrangement ===")
    components = [
        Component("A", 1, 2),
        Component("B", 1, 2),
        Component("C", 1, 2)
    ]
    board = CircuitBoard(1, 6, components)
    if board.solve():
        board.display_solution()
    else:
        print("No solution found!")

def test_performance_comparison():
    """Compare performance with different heuristic combinations"""
    print("\n=== Performance Comparison ===")
    components = [
        Component("A", 2, 2),
        Component("B", 2, 1),
        Component("C", 1, 2),
        Component("D", 1, 1)
    ]
    board_size = (4, 4)
    
    configurations = [
        ("No heuristics", False, False, False),
        ("MRV only", True, False, False),
        ("Degree only", False, True, False),
        ("LCV only", False, False, True),
        ("All heuristics", True, True, True)
    ]
    
    results = []
    for name, use_mrv, use_degree, use_lcv in configurations:
        board = CircuitBoard(board_size[0], board_size[1], components)
        start_time = time.time()
        success = board.solve(use_mrv=use_mrv, use_degree=use_degree, use_lcv=use_lcv)
        solve_time = time.time() - start_time
        
        results.append({
            'config': name,
            'success': success,
            'time': solve_time,
            'nodes': board.solver.nodes_explored if hasattr(board, 'solver') else 0
        })
    
    # Print results table
    print("\nResults:")
    print(f"{'Configuration':<20} {'Success':<10} {'Time (s)':<12} {'Nodes':<10}")
    print("-" * 52)
    for result in results:
        print(f"{result['config']:<20} {str(result['success']):<10} "
              f"{result['time']:.4f}{'s':<8} {result['nodes']:<10}")

def test_edge_cases():
    """Test various edge cases"""
    print("\n=== Test Edge Cases ===")
    
    # Test 1: Empty component list (should raise ValueError)
    print("\nTest 1: Empty component list")
    try:
        CircuitBoard(4, 4, [])
        print("Failed: Should have raised ValueError")
    except ValueError:
        print("Passed: Correctly raised ValueError")
    
    # Test 2: Component larger than board
    print("\nTest 2: Component larger than board")
    try:
        CircuitBoard(3, 3, [Component("A", 4, 2)])
        print("Failed: Should have raised ValueError")
    except ValueError:
        print("Passed: Correctly raised ValueError")
    
    # Test 3: Invalid board dimensions
    print("\nTest 3: Invalid board dimensions")
    try:
        CircuitBoard(0, 4, [Component("A", 1, 1)])
        print("Failed: Should have raised ValueError")
    except ValueError:
        print("Passed: Correctly raised ValueError")

def test_heuristic_configurations():
    """Test different heuristic configurations with various board layouts"""
    print("\n=== Heuristic Configuration Tests ===")
    
    test_cases = [
        {
            'name': "Complex Layout",
            'components': [
                Component("A", 3, 2),
                Component("B", 2, 2),
                Component("C", 1, 3),
                Component("D", 2, 1),
                Component("E", 1, 1)
            ],
            'board_size': (6, 6)
        },
        {
            'name': "L-Shaped Pattern",
            'components': [
                Component("A", 3, 1),
                Component("B", 1, 3),
                Component("C", 2, 2),
                Component("D", 1, 1)
            ],
            'board_size': (5, 5)
        },
        {
            'name': "Dense Packing",
            'components': [
                Component("A", 2, 3),
                Component("B", 3, 2),
                Component("C", 2, 2),
                Component("D", 1, 2),
                Component("E", 2, 1)
            ],
            'board_size': (7, 7)
        }
    ]
    
    heuristic_configs = [
        ("No heuristics", False, False, False),
        ("MRV only", True, False, False),
        ("Degree only", False, True, False),
        ("LCV only", False, False, True),
        ("MRV + Degree", True, True, False),
        ("MRV + LCV", True, False, True),
        ("Degree + LCV", False, True, True),
        ("All heuristics", True, True, True)
    ]
    
    for test_case in test_cases:
        print(f"\nTesting {test_case['name']}:")
        print(f"Board size: {test_case['board_size']}")
        print(f"Number of components: {len(test_case['components'])}")
        print("\nResults:")
        print(f"{'Configuration':<20} {'Success':<10} {'Time (s)':<12} {'Nodes':<10}")
        print("-" * 52)
        
        for name, use_mrv, use_degree, use_lcv in heuristic_configs:
            board = CircuitBoard(test_case['board_size'][0], 
                               test_case['board_size'][1], 
                               test_case['components'])
            
            start_time = time.time()
            success = board.solve(use_mrv=use_mrv, 
                                use_degree=use_degree, 
                                use_lcv=use_lcv)
            solve_time = time.time() - start_time
            
            print(f"{name:<20} {str(success):<10} "
                  f"{solve_time:.4f}{'s':<8} "
                  f"{board.solver.nodes_explored if hasattr(board, 'solver') else 0:<10}")
            
            if success:
                print("\nSolution found:")
                board.display_solution()

def test_comprehensive_heuristics():
    """Test different heuristic and inference combinations with various board layouts"""
    print("\n=== Comprehensive Heuristic Testing ===")
    
    test_cases = [
        {
            'name': "Simple Layout",
            'board_size': (4, 4),
            'components': [
                Component("A", 2, 2),
                Component("B", 2, 1),
                Component("C", 1, 2)
            ]
        },
        {
            'name': "Dense Packing",
            'board_size': (5, 5),
            'components': [
                Component("A", 3, 2),
                Component("B", 2, 3),
                Component("C", 2, 2),
                Component("D", 1, 2),
                Component("E", 2, 1)
            ]
        },
        {
            'name': "Large Board",
            'board_size': (8, 8),
            'components': [
                Component("A", 4, 2),
                Component("B", 3, 3),
                Component("C", 2, 4),
                Component("D", 3, 2),
                Component("E", 2, 2),
                Component("F", 1, 3)
            ]
        }
    ]
    
    configurations = [
        ("No heuristics/inference", False, False, False, False),
        ("MRV only", True, False, False, False),
        ("Degree only", False, True, False, False),
        ("LCV only", False, False, True, False),
        ("AC3 only", False, False, False, True),
        ("MRV + Degree", True, True, False, False),
        ("MRV + LCV", True, False, True, False),
        ("MRV + AC3", True, False, False, True),
        ("Degree + LCV", False, True, True, False),
        ("Degree + AC3", False, True, False, True),
        ("LCV + AC3", False, False, True, True),
        ("All heuristics", True, True, True, True)
    ]
    
    for test_case in test_cases:
        print(f"\n{'-'*60}")
        print(f"Testing {test_case['name']}")
        print(f"Board size: {test_case['board_size']}")
        print(f"Components: {len(test_case['components'])}")
        print(f"{'-'*60}")
        
        results = []
        for name, use_mrv, use_degree, use_lcv, use_ac3 in configurations:
            board = CircuitBoard(test_case['board_size'][0], 
                               test_case['board_size'][1], 
                               test_case['components'])
            
            start_time = time.time()
            success = board.solve(use_mrv=use_mrv, 
                                use_degree=use_degree, 
                                use_lcv=use_lcv)
            solve_time = time.time() - start_time
            
            results.append({
                'config': name,
                'success': success,
                'time': solve_time,
                'nodes': board.solver.nodes_explored if hasattr(board, 'solver') else 0
            })
        
        # Print results table
        print("\nResults:")
        print(f"{'Configuration':<25} {'Success':<10} {'Time (s)':<12} {'Nodes':<10}")
        print("-" * 57)
        for result in results:
            print(f"{result['config']:<25} {str(result['success']):<10} "
                  f"{result['time']:.4f}{'s':<8} {result['nodes']:<10}")

if __name__ == "__main__":
    # Run all tests
    test_basic_layout()
    test_perfect_fit()
    test_impossible_fit()
    test_single_component()
    test_linear_arrangement()
    test_performance_comparison()
    test_edge_cases()
    test_heuristic_configurations()
    test_comprehensive_heuristics()
