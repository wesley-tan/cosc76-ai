from MazeworldProblem import MazeworldProblem
from Maze import Maze
from astar_search import astar_search

class SimultaneousProblem:
    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.num_robots = max(1, len(maze.robotloc) // 2)  # Assume at least 1 robot
        self.start_state = self.create_start_state()
        self.all_actions = ['north', 'south', 'east', 'west', 'stay']

    def create_start_state(self):
        """
        Create the initial state with all robot locations.

        Returns:
            tuple: A tuple representing the initial positions of all robots.
        """
        # Create the initial state with all robot locations
        if not self.maze.robotloc:
            return tuple([0] * (self.num_robots * 2))  # Default position if not specified
        return tuple(self.maze.robotloc)

    def get_successors(self, state):
        """
        Returns all successor states where all robots move simultaneously.

        Args:
            state (tuple): The current state of all robots.

        Returns:
            list: A list of tuples, each containing a new state and the action set that led to it.
        """
        successors = []
        all_combinations = self.generate_combinations(self.num_robots)

        for action_set in all_combinations:
            new_state = list(state)
            valid_move = True

            for i, action in enumerate(action_set):
                robot_x = state[i * 2]
                robot_y = state[i * 2 + 1]
                new_x, new_y = self.apply_action(robot_x, robot_y, action)
                if self.maze.is_floor(new_x, new_y) and not self.is_occupied(new_state, new_x, new_y, i):
                    new_state[i * 2] = new_x
                    new_state[i * 2 + 1] = new_y
                else:
                    valid_move = False
                    break

            if valid_move:
                successors.append((tuple(new_state), action_set))

        return successors

    def generate_combinations(self, num_robots):
        """
        Generate all possible combinations of actions for the robots.
        """
        combinations = []
        self.recursive_combination([], num_robots, combinations)
        return combinations

    def recursive_combination(self, current_combination, num_robots, combinations):
        """
        Helper recursive function to generate all combinations of actions.

        Args:
            current_combination (list): The current combination of actions being built.
            num_robots (int): The number of robots.
            combinations (list): The list to store all generated combinations.
        """
        if len(current_combination) == num_robots:
            combinations.append(current_combination)
            return

        for action in self.all_actions:
            self.recursive_combination(current_combination + [action], num_robots, combinations)

    def apply_action(self, x, y, action):
        """
        Apply an action to a given position.

        Args:
            x (int): The current x-coordinate.
            y (int): The current y-coordinate.
            action (str): The action to apply ('north', 'south', 'east', 'west', or 'stay').

        Returns:
            tuple: The new (x, y) coordinates after applying the action.
        """
        if action == 'north':
            return x, y + 1
        elif action == 'south':
            return x, y - 1
        elif action == 'east':
            return x + 1, y
        elif action == 'west':
            return x - 1, y
        else:
            return x, y  # "stay" action

    def is_occupied(self, state, x, y, current_robot):
        for i in range(self.num_robots):
            if i != current_robot and state[i * 2] == x and state[i * 2 + 1] == y:
                return True
        return False

    def manhattan_heuristic(self, state):
        """
        Calculate the Manhattan distance heuristic for the given state.

        Args:
            state (tuple): The current state of all robots.

        Returns:
            int: The maximum Manhattan distance among all robots to their respective goals.
        """
        max_distance = 0
        for i in range(self.num_robots):
            robot_x = state[i * 2]
            robot_y = state[i * 2 + 1]
            goal_x = self.goal_locations[i * 2]
            goal_y = self.goal_locations[i * 2 + 1]
            max_distance = max(max_distance, abs(robot_x - goal_x) + abs(robot_y - goal_y))
        return max_distance

    def null_heuristic(self, state):
        return 0

    def goal_test(self, state):
        return state == self.goal_locations

    def get_transition_cost(self, next_state, current_state):
        """
        Calculate the transition cost between two states.

        Args:
            next_state (tuple): The state being transitioned to.
            current_state (tuple): The current state.

        Returns:
            int: The maximum number of moves any robot made (representing the time cost).
        """
        max_distance = 0
        for i in range(0, len(current_state), 2):
            x_curr, y_curr = current_state[i], current_state[i + 1]
            x_next, y_next = next_state[i], next_state[i + 1]
            max_distance = max(max_distance, abs(x_curr - x_next) + abs(y_curr - y_next))
        return max_distance

    def __str__(self):
        return f"Multi-Robot Simultaneous Problem: {self.num_robots} robots, Goal: {self.goal_locations}"

def run_test_case(maze_file, test_name, goal_locations=None):
    """
    Run a test case for the SimultaneousProblem.

    Args:
        maze_file (str): The filename of the maze to load.
        test_name (str): A name for the test case.
        goal_locations (tuple, optional): The goal locations for the robots. If None, uses the initial robot locations.

    Returns:
        list or None: The solution path if found, None if there was an error or no solution.

    Prints:
        Information about the test case, including start state, goal state, and search results.
    """
    try:
        maze = Maze(maze_file)
        if not maze.robotloc:
            print(f"{test_name}: No robots found in the maze.")
            return None
        
        if goal_locations is None:
            goal_locations = tuple(maze.robotloc)  
        
        problem = SimultaneousProblem(maze, goal_locations)
        result = astar_search(problem, problem.manhattan_heuristic)
        print(f"{test_name}:")
        print(f"Start state: {problem.start_state}")
        print(f"Goal state: {goal_locations}")
        print(result)
        return result.path
    except FileNotFoundError:
        print(f"{test_name}: Maze file '{maze_file}' not found.")
        return None

# Test cases
run_test_case("maze1.maz", "Test case 1: Small maze", (2, 2))
run_test_case("maze2.maz", "Test case 2: Medium maze", (3, 3))
run_test_case("maze3.maz", "Test case 3: Large maze", (1, 4, 1, 3, 1, 2))
