# COSC 76 Fall 2024
# Wesley Tan
# PA2 Mazeworld
# test_mazeworld.py

from MazeworldProblem import MazeworldProblem
from Maze import Maze
from astar_search import astar_search

def run_test_case(maze, goal, test_name):
    print(f"\n{test_name}")
    # print("Maze:")
    # print(maze)
    mp = MazeworldProblem(maze, goal)
    print("Start state:", mp.start_state)
    print("Goal:", goal)

    print("\nA* search with null heuristic:")
    result_null = astar_search(mp, mp.null_heuristic)
    print(result_null)

    print("\nA* search with Manhattan distance heuristic:")
    result_manhattan = astar_search(mp, mp.manhattan_heuristic)
    print(result_manhattan)

    if result_manhattan.path:
        print("\nAnimating solution path:")
        mp.animate_path(result_manhattan.path)

# Test case 1: Original test (maze3.maz)
test_maze3 = Maze("maze3.maz")
run_test_case(test_maze3, (1, 4, 1, 3, 1, 2), "Test case 1: Original test (maze3.maz)")

# Test case 2: Single robot (maze1.maz)
test_maze1 = Maze("maze2.maz")
run_test_case(test_maze1, (2,2), "Test case 2: Single robot (maze2.maz)")

# Test case 3: Robots swapping positions (maze_swap.maz)
test_maze_swap = Maze("maze_swap.maz")
run_test_case(test_maze_swap, (3, 1, 1, 3), "Test case 3: Robots swapping positions (maze_swap.maz)")

# Test case 4: Unsolvable problem (maze2.maz)
test_maze_unsolvable = Maze("maze2.maz")
run_test_case(test_maze_unsolvable, (3, 3), "Test case 4: Unsolvable problem (maze2.maz)")