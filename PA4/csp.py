# Wesley Tan
# COSC 76 PA 4

from typing import List, Dict, Tuple, Optional, Set, Callable

class CSP:
    def __init__(self, num_variables: int, domains: List[Set[int]]):
        self.num_variables = num_variables
        self.domains = domains
        self.constraints: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}

    def add_constraint(self, var1: int, var2: int, allowed_pairs: List[Tuple[int, int]]):
        """Add constraint between two variables with allowed value pairs"""
        if (var1, var2) not in self.constraints:
            self.constraints[(var1, var2)] = []
        self.constraints[(var1, var2)].extend(allowed_pairs)

    def is_consistent(self, var: int, value: int, assignment: List[Optional[int]]) -> bool:
        """Check if assigning value to var is consistent with current assignment"""
        for (var1, var2), allowed_pairs in self.constraints.items():
            if var == var1 and assignment[var2] is not None:
                if (value, assignment[var2]) not in allowed_pairs:
                    return False
            elif var == var2 and assignment[var1] is not None:
                if (assignment[var1], value) not in allowed_pairs:
                    return False
        return True

    def backtrack(self, assignment: Optional[List[Optional[int]]] = None) -> Optional[List[Optional[int]]]:
        """Find solution using simple backtracking search"""
        if assignment is None:
            assignment = [None] * self.num_variables

        if all(val is not None for val in assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment[var] = None

        return None

    def select_unassigned_variable(self, assignment: List[Optional[int]]) -> int:
        for i in range(self.num_variables):
            if assignment[i] is None:
                return i
        raise Exception("No unassigned variables found")

class CSPSolver:
    def __init__(self, csp: CSP, use_mrv=False, use_degree=False, use_lcv=False, use_ac3=True):

        """
        Initialize CSP Solver with optional heuristics
        
        - MRV (Minimum Remaining Values): Choose variable with fewest legal values
        - Degree: Choose variable involved in most constraints with unassigned variables
        - LCV (Least Constraining Value): Order domain values by how many options they eliminate
        - AC3: Arc consistency 
        """

        self.csp = csp
        self.use_mrv = use_mrv
        self.use_degree = use_degree
        self.use_lcv = use_lcv
        self.use_ac3 = use_ac3
        self.nodes_explored = 0

    def backtrack(self, assignment: Optional[List[Optional[int]]] = None) -> Optional[List[Optional[int]]]:
        """Find solution using backtracking with optional heuristics"""
        if assignment is None:
            assignment = [None] * self.csp.num_variables
            # Run AC3 as a preprocessing step if enabled
            if self.use_ac3 and not self.ac3():
                return None
            
        # Special case: if there are no variables, return empty solution
        if self.csp.num_variables == 0:
            return {}
            
        # Return assignment if complete
        if all(val is not None for val in assignment):
            return assignment
            
        # Select unassigned variable
        var = self.select_unassigned_variable(assignment)
        
        # Try each value in the domain
        for value in self.order_domain_values(var, assignment):
            self.nodes_explored += 1
            
            # Check if value is consistent with current assignment
            if self.csp.is_consistent(var, value, assignment):
                # Add to assignment
                assignment[var] = value
                
                # Run AC3 after each assignment if enabled
                if self.use_ac3:
                    # Save domain state
                    saved_domains = [{val for val in domain} for domain in self.csp.domains]
                    
                    # If AC3 fails, restore domains and try next value
                    if not self.ac3():
                        self.csp.domains = saved_domains
                        assignment[var] = None
                        continue
                
                # Recursive call
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                
                # If no solution found, undo assignment and restore domains
                assignment[var] = None
                if self.use_ac3:
                    self.csp.domains = saved_domains
                
        return None

    def select_unassigned_variable(self, assignment: List[Optional[int]]) -> int:
        """Choose next unassigned variable using MRV and degree heuristics if enabled"""
        unassigned_vars = [v for v in range(self.csp.num_variables) if assignment[v] is None]
        
        if self.use_mrv:
            # MRV (Minimum Remaining Values) Heuristic
            def count_legal_values(var):
                return len([val for val in self.csp.domains[var] 
                          if self.csp.is_consistent(var, val, assignment)])
            
            if self.use_degree:
                # Use degree as tiebreaker for MRV
                def count_unassigned_neighbors(var):
                    return sum(1 for neighbor in self.neighbors(var) 
                             if assignment[neighbor] is None)
                
                return min(unassigned_vars,
                         key=lambda var: (count_legal_values(var), 
                                        -count_unassigned_neighbors(var)))
            
            return min(unassigned_vars, key=count_legal_values)
        
        elif self.use_degree:
            # Standalone degree heuristic
            def count_unassigned_neighbors(var):
                return sum(1 for neighbor in self.neighbors(var) 
                         if assignment[neighbor] is None)
            
            return max(unassigned_vars, key=count_unassigned_neighbors)
        
        return unassigned_vars[0]

    def order_domain_values(self, var: int, assignment: List[Optional[int]]) -> List[int]:
        """Order domain values using LCV heuristic if enabled"""
        if self.use_lcv:
            # LCV (Least Constraining Value) Heuristic
            # Orders values by how many options they eliminate for neighboring variables
            # Tries values that rule out the fewest choices for other variables first
            # Example: If value 1 conflicts with 5 other assignments and value 2 conflicts
            # with only 2, try value 2 first
            return sorted(self.csp.domains[var],
                        key=lambda val: self.count_conflicts(var, val, assignment))
        
        return list(self.csp.domains[var])

    def count_conflicts(self, var: int, value: int, assignment: List[Optional[int]]) -> int:
        """Count number of conflicts when assigning value to var"""
        conflicts = 0
        for (var1, var2), allowed_pairs in self.csp.constraints.items():
            # Check conflicts in both directions of constraints
            if var == var1 and assignment[var2] is not None:
                if (value, assignment[var2]) not in allowed_pairs:
                    conflicts += 1
            elif var == var2 and assignment[var1] is not None:
                if (assignment[var1], value) not in allowed_pairs:
                    conflicts += 1
        return conflicts

    def ac3(self) -> bool:
        """Enforce arc consistency on CSP"""
        # AC3 (Arc Consistency) Algorithm
        # Enforces arc consistency by ensuring that every value in each variable's domain
        # has at least one compatible value in each neighboring variable's domain
        # This prunes invalid values early, reducing the search space
        # Example: If X must be less than Y, and X={1,2,3} and Y={2}, then AC3 would
        # remove 2,3 from X's domain since they can never satisfy the constraint
        queue = [(var1, var2) for var1, var2 in self.csp.constraints]
        
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if not self.csp.domains[xi]:
                    return False
                for xk in self.neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi: int, xj: int) -> bool:
        """Remove inconsistent values from xi's domain relative to xj"""
        revised = False
        for x in set(self.csp.domains[xi]):
            # Check if there exists any valid value in xj's domain
            has_support = False
            for y in self.csp.domains[xj]:
                # Check both directions of constraints
                forward = (x, y) in self.csp.constraints.get((xi, xj), [])
                backward = (y, x) in self.csp.constraints.get((xj, xi), [])
                if forward or backward:
                    has_support = True
                    break
            if not has_support:
                self.csp.domains[xi].remove(x)
                revised = True
        return revised

    def neighbors(self, var: int) -> List[int]:
        """Get all variables that share constraints with var"""
        return [var2 for (var1, var2) in self.csp.constraints if var1 == var] + \
               [var1 for (var1, var2) in self.csp.constraints if var2 == var]

def create_generic_csp(variables: List[str], domains: Dict[str, Set[int]], constraints: List[Tuple[str, str, Callable]]) -> CSP:
    """Create CSP from variables, domains and constraints"""
    var_index = {var: idx for idx, var in enumerate(variables)}
    csp = CSP(len(variables), [domains[var] for var in variables])

    for var1, var2, constraint in constraints:
        allowed_pairs = [(val1, val2) for val1 in domains[var1] for val2 in domains[var2] if constraint(val1, val2)]
        csp.add_constraint(var_index[var1], var_index[var2], allowed_pairs)

    return csp
