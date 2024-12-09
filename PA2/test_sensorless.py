# COSC 76 Fall 2024 
# Wesley Tan
# PA2 Mazeworld
# test_sensorless.py

from Maze import Maze
from SensorlessProblem import SensorlessProblem
from astar_search import astar_search

def run_test_case(maze_file, test_name):
    print(f"\n{test_name}")
    maze = Maze(maze_file)
    problem = SensorlessProblem(maze)
    print(f"Initial belief state size: {len(problem.start_state)}")

    result1 = astar_search(problem, problem.manhattan_heuristic)
    print(result1)

    result2 = astar_search(problem, problem.custom_heuristic)
    print(result2)

    result3 = astar_search(problem, problem.null_heuristic)
    print(result3)

    if result1.path:
        print("Animating solution path:")
        problem.animate_path(result1.path)

    if result2.path:
        print("Animating solution path:")
        problem.animate_path(result2.path)

    if result3.path:
        print("Animating solution path:")
        problem.animate_path(result3.path)
    
    return

# Test case 1: Small maze
run_test_case("maze1.maz", "Test case 1: Maze 1")

# Test case 2: Medium maze
run_test_case("maze2.maz", "Test case 2: Maze 2")

# Test case 3: Large maze
run_test_case("maze3.maz", "Test case 3: Maze 3")
