# COSC 76 Fall 2024
# Wesley Tan
# PA2 Mazeworld
# astar_search.py

from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        return self.transition_cost + self.heuristic

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result

def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    while pqueue:
        current_node = heappop(pqueue)
        solution.nodes_visited += 1

        if search_problem.goal_test(current_node.state):
            solution.path = backchain(current_node)
            solution.cost = current_node.transition_cost
            return solution

        successors = search_problem.get_successors(current_node.state)
        for successor_state, action in successors:
            successor_cost = current_node.transition_cost + search_problem.get_transition_cost(successor_state, current_node.state)
            
            if successor_state not in visited_cost or successor_cost < visited_cost[successor_state]:
                visited_cost[successor_state] = successor_cost
                successor_node = AstarNode(successor_state, heuristic_fn(successor_state), current_node, successor_cost)
                heappush(pqueue, successor_node)

    return solution
