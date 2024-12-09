
from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
# keep track of current depth for the dfs, and point to parent node

class SearchNode:
    """
    Each SearchNode wraps a state object and keeps track of the path.
    It contains a reference to its parent node and the action taken to reach this state.
    """

    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state   
        self.parent = parent   
        self.action = action    
        self.cost = cost          

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

# you might write other helper functions, too. For example,
# I like to separate out backchaining, and the dfs path checking functions

def backchain(node):
    """
    Reconstruct the path from the start state to the given node.

    Args:
    node (SearchNode): The end node of the path.

    Returns:
    list: A list of states representing the path from start to end.
    """
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

def bfs_search(search_problem):
    """
    Perform a breadth-first search on the given search problem.

    Args:
    search_problem: An object representing the search problem with methods:
        - start_state: The initial state.
        - is_goal_state(state): Returns True if the given state is a goal state.
        - get_successors(state): Returns a list of successor states.

    Returns:
    SearchSolution: An object containing the solution path and search statistics.
    """
    start_state = search_problem.start_state
    root = SearchNode(state=start_state)
    frontier = deque([root])  # Queue for BFS
    visited = set()
    solution = SearchSolution(search_problem, "BFS")

    while frontier:
        node = frontier.popleft()
        state = node.state

        if state in visited:
            continue
        visited.add(state)
        solution.nodes_visited += 1

        if search_problem.is_goal_state(state):
            # Goal found, reconstruct the path
            solution.path = backchain(node)
            return solution

        successors = search_problem.get_successors(state)
        for successor_state in successors:
            if successor_state not in visited:
                child_node = SearchNode(successor_state, parent=node)
                frontier.append(child_node)

    # No solution found
    return solution

# Don't forget that your dfs function should be recursive and do path checking,
# rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded

def dfs_search(search_problem, node=None, solution=None, path=None):
    """
    Perform a depth-first search on the given search problem.

    Args:
    search_problem: An object representing the search problem.
    node (SearchNode, optional): The current node being explored. Defaults to None.
    solution (SearchSolution, optional): The current solution object. Defaults to None.
    path (set, optional): A set of states in the current path. Defaults to None.

    Returns:
    SearchSolution: An object containing the solution path and search statistics.
    """
    if node is None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
        path = set()

    solution.nodes_visited += 1

    # Base Case: Goal State
    # Memory is polynomial
    if search_problem.is_goal_state(node.state):
        solution.path = backchain(node)
        return solution

    # Path checking: avoid cycles by checking the current path
    if node.state in path:
        return solution  # Return the solution object even if no solution found along this path

    path.add(node.state)

    successors = search_problem.get_successors(node.state)
    for successor_state in successors:
        child_node = SearchNode(successor_state, parent=node)
        # Recursively call dfs_search
        result = dfs_search(search_problem, child_node, solution, path)
        if result.path:
            return result  # Goal found

    path.remove(node.state)  # Backtrack
    return solution  # Return the solution object

# Adapted from Page 88, Russell, S. J., & Norvig, P. (2020)
def ids_search(search_problem, depth_limit=100):
    """
    Perform an iterative deepening search on the given search problem.

    Args:
    search_problem: An object representing the search problem.
    depth_limit (int, optional): The maximum depth to search. Defaults to 100.

    Returns:
    SearchSolution: An object containing the solution path and search statistics.
    """
    solution = SearchSolution(search_problem, "IDS")

    for depth in range(depth_limit):
        path = set()
        node = SearchNode(search_problem.start_state)
        result = depth_limited_search(node, path, depth, solution, search_problem)
        if result:
            return solution  # Goal found
    # No solution found within the depth limit
    return solution

def depth_limited_search(node, path, limit, solution, search_problem):
    """
    Perform a depth-limited search as part of the iterative deepening search.

    Args:
    node (SearchNode): The current node being explored.
    path (set): A set of states in the current path.
    limit (int): The depth limit for this search.
    solution (SearchSolution): The current solution object.
    search_problem: An object representing the search problem.

    Returns:
    bool: True if a goal state is found within the depth limit, False otherwise.
    """
    solution.nodes_visited += 1
    if search_problem.is_goal_state(node.state):
        solution.path = backchain(node)
        return True
    if limit <= 0:
        return False
    if node.state in path:
        return False

    path.add(node.state)
    successors = search_problem.get_successors(node.state)
    for successor_state in successors:
        child_node = SearchNode(successor_state, parent=node)
        if depth_limited_search(child_node, path, limit - 1, solution, search_problem):
            return True
    path.remove(node.state)  # Backtrack
    return False

