# COSC 76 Fall 2024
# Wesley Tan
# PA2 Mazeworld
# SearchSolution.py

class SearchSolution:
    """
    A class to represent the solution of a search problem.
    """

    def __init__(self, problem, search_method):
        self.problem_name = str(problem)
        self.search_method = search_method
        self.path = []
        self.nodes_visited = 0
        self.cost = 0

    def __str__(self):
        string = "----\n"
        string += f"{self.problem_name}\n"
        string += f"attempted with search method {self.search_method}\n"

        if self.path:
            string += f"number of nodes visited: {self.nodes_visited}\n"
            string += f"solution length: {len(self.path)}\n"
            string += f"cost: {self.cost}\n"
            string += f"path: {self.path}\n"
        else:
            string += f"no solution found after visiting {self.nodes_visited} nodes\n"

        return string
