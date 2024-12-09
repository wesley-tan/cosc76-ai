# COSC 76 Fall 2024
# Wesley Tan
# PA2 Mazeworld
# SensorlessProblem.py

from Maze import Maze
from time import sleep
from astar_search import astar_search
from itertools import combinations, product

class SensorlessProblem:
    def __init__(self, maze):
        """
        Initialize the SensorlessProblem.
        
        Args:
            maze (Maze): The maze object representing the environment.
        
        Initializes:
            self.maze: The maze object.
            self.start_state: A frozenset of all possible initial locations.
            self.maze.robotloc: The first location from start_state, or None if empty.
        """
        self.maze = maze
        self.start_state = frozenset(self.get_all_possible_locations())
        self.maze.robotloc = next(iter(self.start_state)) if self.start_state else None

    def get_all_possible_locations(self):
        """
        Get all possible floor locations in the maze.
        
        Returns:
            list: A list of tuples (x, y) representing all floor locations.
        """
        return [(x, y) for x in range(self.maze.width) for y in range(self.maze.height) if self.maze.is_floor(x, y)]

    def get_successors(self, state):
        """
        Get all possible successor states from the current state.
        
        Args:
            state (frozenset): The current state (set of possible locations).
        
        Returns:
            list: A list of tuples (new_state, action) representing successors.
        """
        successors = []
        actions = ['north', 'south', 'east', 'west']
        for action in actions:
            new_state = frozenset(self.move(loc, action) for loc in state)
            if new_state != state:
                successors.append((new_state, action))
        return successors

    def move(self, loc, action):
        """
        Attempt to move from a given location in a specified direction.
        
        Args:
            loc (tuple): The current location (x, y).
            action (str): The direction to move ('north', 'south', 'east', 'west').
        
        Returns:
            tuple: The new location after the move, or the original location if the move is invalid.
        """
        x, y = loc
        if action == 'north' and self.maze.is_floor(x, y+1):
            return (x, y+1)
        elif action == 'south' and self.maze.is_floor(x, y-1):
            return (x, y-1)
        elif action == 'east' and self.maze.is_floor(x+1, y):
            return (x+1, y)
        elif action == 'west' and self.maze.is_floor(x-1, y):
            return (x-1, y)
        return (x, y)  # Stay in place if move is not possible
    
    def get_transition_cost(self, next_state, current_state):
        # Assuming uniform cost for all moves
        return 1

    def goal_test(self, state):
        return len(state) == 1

    # Heuristics
    
    def manhattan_heuristic(self, state):
        if len(state) <= 1:
            return 0
        # Calculate the maximum Manhattan distance between any two points in the state
        return max(abs(x1-x2) + abs(y1-y2) for (x1, y1), (x2, y2) in combinations(state, 2))

    def custom_heuristic(self, state):
        # This heuristic estimates the number of moves needed to reduce the state to a single location
        return len(state) - 1

    def null_heuristic(self, state):
        return 0

    def __str__(self):
        return f"Blind robot problem: maze size {self.maze.width}x{self.maze.height}"

    def animate_path(self, path):
        """
        Animate the solution path in the maze.
        
        Args:
            path (list): A list of states representing the solution path.
        
        Prints the maze state for each step in the path with a 1-second delay between steps.
        """
        # reset the robot locations in the maze
        self.maze.robotloc = []

        for state in path:
            print(str(self))
            self.maze.robotloc = []
            # self.maze.robotloc = next(iter(state))

            # adapted this slightly to print multiple possible locations
            for loc in state:
                self.maze.robotloc.extend([loc[0], loc[1]])
            sleep(1)

            print(str(self.maze))

    def state_to_string(self, state):
        """
        Convert a state to a string representation.
        
        Args:
            state (frozenset): The state to convert.
        
        Returns:
            str: A string representation of the state, listing all locations.
        """
        return ', '.join([f'({x}, {y})' for x, y in state])

# Test code
if __name__ == "__main__":
    test_maze2 = Maze("maze2.maz")
    test_problem = SensorlessProblem(test_maze2)

    print("Test case 1: Basic functionality")
    print("Initial belief state:", test_problem.start_state)
    print("Number of possible initial locations:", len(test_problem.start_state))

    print("\nTest case 2: Successor function")
    successors = test_problem.get_successors(test_problem.start_state)
    print("Number of successors:", len(successors))
    print("First successor:", successors[0])

    print("\nTest case 3: Goal test")
    print("Is initial state a goal?", test_problem.goal_test(test_problem.start_state))
    single_location = frozenset([(1, 1)])
    print("Is single location a goal?", test_problem.goal_test(single_location))

    print("\nTest case 4: Heuristics")
    print("Blind robot heuristic for initial state:", test_problem.manhattan_heuristic(test_problem.start_state))
    print("Custom heuristic for initial state:", test_problem.custom_heuristic(test_problem.start_state))
    print("Null heuristic for initial state:", test_problem.null_heuristic(test_problem.start_state))

    print("\nTest case 5: A* search")
    result = astar_search(test_problem, test_problem.manhattan_heuristic)
    print(result)

    if result.path:
        print("\nTest case 6: Solution path")
        for i, state in enumerate(result.path):
            print(f"Step {i}: {test_problem.state_to_string(state)}")

        print("\nTest case 7: Animate solution")
        test_problem.animate_path(result.path)
