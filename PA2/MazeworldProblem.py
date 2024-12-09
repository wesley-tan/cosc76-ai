# COSC 76 Fall 2024
# Wesley Tan
# PA2 Mazeworld
# MazeworldProblem.py

from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        """
        Initialize a new instance of the MazeworldProblem class.

        Args:
            maze: An instance of the Maze class representing the maze environment.
            goal_locations: A tuple containing the goal locations for the robots.
        """
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = self.create_start_state()
        self.num_robots = max(1, len(maze.robotloc) // 2)  # Ensure at least 1 robot

    def create_start_state(self):
        """
        Creates the initial state of the problem, including the turn and the positions of all robots.

        Returns:
            A tuple representing the initial state, where the first element is the turn (0) 
            and the subsequent elements are the robot locations.
        """
        if not self.maze.robotloc:
            return (0, 1, 0)  # Default position for a single robot if not specified
        return (0,) + tuple(self.maze.robotloc)

    def get_successors(self, state):
        """
        Generates all possible successor states from the current state.

        Args:
            state: A tuple representing the current state of the robots.

        Returns:
            A list of tuples, each containing a new state and the action that led to it.
        """
        successors = []
        current_turn = state[0]
        next_turn = (current_turn + 1) % self.num_robots

        # Only move the robot whose turn it is
        robot_index = current_turn
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:  # (0, 0) for "stay" action
            new_x = state[robot_index*2 + 1] + dx
            new_y = state[robot_index*2 + 2] + dy
            if self.maze.is_floor(new_x, new_y) and not self.is_occupied(state, new_x, new_y, robot_index):
                new_state = list(state)
                new_state[0] = next_turn
                new_state[robot_index*2 + 1] = new_x
                new_state[robot_index*2 + 2] = new_y
                action = self.get_action_name(dx, dy)
                successors.append((tuple(new_state), action))
        return successors

    def get_action_name(self, dx, dy):
        """
        Maps the change in coordinates to a corresponding action name.

        Args:
            dx: The change in the x-coordinate.
            dy: The change in the y-coordinate.

        Returns:
            A string representing the action name (e.g., "north", "south", "east", "west", or "stay").
        """
        if dx == -1 and dy == 0:
            return "west"
        elif dx == 1 and dy == 0:
            return "east"
        elif dx == 0 and dy == -1:
            return "south"
        elif dx == 0 and dy == 1:
            return "north"
        else:
            return "stay"

    def is_occupied(self, state, x, y, current_robot):
        """
        Checks if a given position is occupied by another robot.

        Args:
            state: The current state of all robots.
            x: The x-coordinate to check.
            y: The y-coordinate to check.
            current_robot: The index of the robot currently being moved.

        Returns:
            True if the position is occupied by another robot, False otherwise.
        """
        for i in range(self.num_robots):
            if i != current_robot and state[i*2 + 1] == x and state[i*2 + 2] == y:
                return True
        return False

    def __str__(self):
        return f"Mazeworld problem: {self.num_robots} robots, Goal: {self.goal_locations}\n{self.maze}"

    def animate_path(self, path):
        """
        Animates the solution path by updating the robot locations in the maze and printing the maze state at each step.

        Args:
            path: A list of states representing the solution path.

        Returns:
            None.
        """
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))

    def goal_test(self, state):
        # Ignore the first element (turn) when comparing
        return tuple(state[1:]) == self.goal_locations

    # Heuristics
    
    def manhattan_heuristic(self, state):
        """
        Calculates the Manhattan distance heuristic for the given state.

        Args:
            state: A tuple representing the current state of the robots.

        Returns:
            A float representing the average Manhattan distance of all robots to their respective goal locations.
        """
        total_distance = 0
        for i in range(self.num_robots):
            robot_x = state[i*2 + 1]
            robot_y = state[i*2 + 2]
            goal_x = self.goal_locations[i*2]
            goal_y = self.goal_locations[i*2 + 1]
            total_distance += abs(robot_x - goal_x) + abs(robot_y - goal_y)
        return total_distance / self.num_robots

    def null_heuristic(self, state):
        return 0

    def get_transition_cost(self, next_state, current_state):
        if next_state[1:] == current_state[1:]: # if the robot positions are the same, the cost is 0
            return 0
        return 1
        
## A bit of test code to verify that things work as expected.

if __name__ == "__main__":
    # Test case 1: Original test
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print("Test case 1:")
    print("Start state:", test_mp.start_state)
    print("Successors of start state:", test_mp.get_successors(test_mp.start_state))
    print("Successors of (0, 1, 0, 1, 2, 2, 1):", test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))

    # Test case 2: Single robot
    test_maze1 = Maze("maze1.maz")
    test_mp_single = MazeworldProblem(test_maze1, (3, 3))
    print("\nTest case 2 (Single robot):")
    print("Start state:", test_mp_single.start_state)
    print("Successors of start state:", test_mp_single.get_successors(test_mp_single.start_state))
    
    # Test case 4: Goal state test
    print("\nTest case 4 (Goal state test):")
    print("Is start state a goal?", test_mp.goal_test(test_mp.start_state))
    print("Is goal state a goal?", test_mp.goal_test((2,) + test_mp.goal_locations))

    # Test case 5: Edge cases
    print("\nTest case 5 (Edge cases):")
    print("Successors of state with robot at maze edge:", 
          test_mp.get_successors((0, 1, 4, 1, 3, 1, 2)))
    print("Successors of state with robots adjacent:", 
          test_mp.get_successors((1, 1, 1, 1, 2, 1, 3)))

    # Test case 6: __str__ method
    print("\nTest case 6 (__str__ method):")
    print(str(test_mp))
    print(str(test_mp_single))
