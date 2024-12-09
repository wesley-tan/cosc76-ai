class FoxProblem:
    def __init__(self, start_state):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        # Store total number of chickens and foxes
        self.total_chickens = start_state[0]
        self.total_foxes = start_state[1]

    def get_successors(self, state):
        """
        Generate all valid successor states from the current state.

        This function considers all possible moves (1 or 2 animals in the boat)
        and generates new states by applying these moves. It then filters out
        illegal states.

        Args:
            state (Tuple[int, int, int]): The current state.

        Returns:
            List[Tuple[int, int, int]]: A list of all valid successor states.
        """
        successors = []
        chickens, foxes, boat = state
        boat_new = 1 - boat  # Toggle boat position (1 to 0 or 0 to 1)

        # Define possible moves based on boat capacity and rules
        possible_moves = []
        if boat == 1:  # Boat is on left bank
            # Possible moves from left to right
            possible_moves = [
                (2, 0),   # Move 2 chickens
                (1, 0),   # Move 1 chicken
                (1, 1),   # Move 1 chicken and 1 fox
                (0, 1),   # Move 1 fox
                (0, 2),   # Move 2 foxes
            ]
        else:  # Boat is on right bank
            # Possible moves from right to left
            possible_moves = [
                (-2, 0),  # Move 2 chickens back
                (-1, 0),  # Move 1 chicken back
                (-1, -1), # Move 1 chicken and 1 fox back
                (0, -1),  # Move 1 fox back
                (0, -2),  # Move 2 foxes back
            ]

        # Generate new states by applying possible moves
        for move in possible_moves:
            new_chickens = chickens - move[0] if boat == 1 else chickens - move[0]
            new_foxes = foxes - move[1] if boat == 1 else foxes - move[1]
            new_state = (new_chickens, new_foxes, boat_new)
            if self.is_legal_state(new_state):
                successors.append(new_state)
        return successors

    def is_legal_state(self, state):
        """
        Check if a state is legal.

        Args:
            state (Tuple[int, int, int]): The state to check.

        Returns:
            bool: True if the state is legal, False otherwise.
        """
        chickens, foxes, boat = state
        chickens_right = self.total_chickens - chickens
        foxes_right = self.total_foxes - foxes

        # Check for invalid numbers
        if chickens < 0 or foxes < 0 or \
           chickens > self.total_chickens or foxes > self.total_foxes:
            return False

        # Check if chickens are safe on the left bank
        if chickens > 0 and foxes > chickens:
            return False

        # Check if chickens are safe on the right bank
        if chickens_right > 0 and foxes_right > chickens_right:
            return False

        return True

    def is_goal_state(self, state):
        """
        Check if the current state is the goal state.
        
        Args:
            state (Tuple[int, int, int]): The current state.

        Returns:
            bool: True if the state is the goal state, False otherwise.
        """
        return state == self.goal_state

    def __str__(self):
        return f"Chickens and foxes problem: Start State {self.start_state}"
