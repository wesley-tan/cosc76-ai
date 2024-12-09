# Wesley Tan
# COSC 76 PA5

import random
import logging

from typing import Dict, List, Set, Optional
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s',
    datefmt='%H:%M:%S'
)

class SAT:
    def __init__(self, cnf_filename: str):
        self.variables: Set[int] = set()
        self.clauses: List[List[int]] = []
        self.assignment: Dict[int, bool] = {}
        self.best_assignment: Dict[int, bool] = {}
        self.best_satisfied_count: int = 0
        
        # Optimization: Track which clauses each variable appears in
        self.var_to_clauses: Dict[int, List[int]] = defaultdict(list)
        
        self.load_cnf(cnf_filename)
        logging.info(f"Initialized SAT solver with {len(self.variables)} variables and {len(self.clauses)} clauses")
    
    def load_cnf(self, filename: str) -> None:
        """Load CNF formula from file with optimized indexing"""
        with open(filename, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                    
                clause = [int(lit) for lit in line.split()]
                if clause:
                    clause_idx = len(self.clauses)
                    self.clauses.append(clause)
                    
                    for literal in clause:
                        var = abs(literal)
                        self.variables.add(var)
                        self.var_to_clauses[var].append(clause_idx)
    
    def evaluate_clause(self, clause: List[int], assignment: Dict[int, bool]) -> bool:
        """Evaluate a single clause"""
        return any((literal > 0 and assignment[abs(literal)]) or
                  (literal < 0 and not assignment[abs(literal)])
                  for literal in clause)
    
    def count_satisfied_clauses(self, assignment: Dict[int, bool]) -> int:
        """Count number of satisfied clauses"""
        return sum(1 for clause in self.clauses if self.evaluate_clause(clause, assignment))
    
    def get_unsatisfied_clauses(self, assignment: Dict[int, bool]) -> List[int]:
        """Get indices of unsatisfied clauses"""
        return [i for i, clause in enumerate(self.clauses) 
                if not self.evaluate_clause(clause, assignment)]
    
    def calculate_make_break(self, var: int, assignment: Dict[int, bool]) -> tuple[int, int]:
        """Calculate make and break counts for flipping a variable"""
        make_count = 0
        break_count = 0
        
        test_assignment = assignment.copy()
        test_assignment[var] = not test_assignment[var]
        
        for clause_idx in self.var_to_clauses[var]:
            clause = self.clauses[clause_idx]
            before = self.evaluate_clause(clause, assignment)
            after = self.evaluate_clause(clause, test_assignment)
            
            if before and not after:
                break_count += 1
            elif not before and after:
                make_count += 1
                
        return make_count, break_count
    
    def walksat(self, max_tries: int = 100, max_flips: int = 100000, p: float = 0.3) -> bool:
        for try_num in range(max_tries):
            # Initialize random assignment
            assignment = {var: random.choice([True, False]) for var in self.variables}
            
            current_satisfied = self.count_satisfied_clauses(assignment)
            if current_satisfied > self.best_satisfied_count:
                self.best_satisfied_count = current_satisfied
                self.best_assignment = assignment.copy()
            
            for flip in range(max_flips):
                if current_satisfied == len(self.clauses):
                    self.assignment = assignment
                    if self.validate_solution():
                        return True
                    return False
                
                # Progress logging
                if flip % 10000 == 0:
                    progress = (current_satisfied / len(self.clauses)) * 100
                    logging.info(f"Try {try_num + 1}, Flip {flip}: {current_satisfied}/{len(self.clauses)} "
                               f"clauses satisfied ({progress:.1f}%)")
                
                # Get unsatisfied clauses
                unsatisfied = self.get_unsatisfied_clauses(assignment)
                clause = self.clauses[random.choice(unsatisfied)]
                
                if random.random() < p:
                    # Random walk
                    var = abs(random.choice(clause))
                else:
                    # Greedy selection
                    best_score = float('-inf')
                    candidates = []
                    
                    for lit in clause:
                        var = abs(lit)
                        make, break_count = self.calculate_make_break(var, assignment)
                        score = make - break_count
                        
                        if score > best_score:
                            best_score = score
                            candidates = [var]
                        elif score == best_score:
                            candidates.append(var)
                    
                    var = random.choice(candidates)
                
                # Flip the chosen variable
                assignment[var] = not assignment[var]
                current_satisfied = self.count_satisfied_clauses(assignment)
                
                if current_satisfied > self.best_satisfied_count:
                    self.best_satisfied_count = current_satisfied
                    self.best_assignment = assignment.copy()
        
        self.assignment = self.best_assignment
        return False

    def gsat(self, max_tries: int = 100, max_flips: int = 1000, h: float = 0.3) -> bool:
        for try_num in range(max_tries):
            # Initialize random assignment
            assignment = {var: random.choice([True, False]) for var in self.variables}
            
            current_satisfied = self.count_satisfied_clauses(assignment)
            if current_satisfied > self.best_satisfied_count:
                self.best_satisfied_count = current_satisfied
                self.best_assignment = assignment.copy()
            
            for flip in range(max_flips):
                if current_satisfied == len(self.clauses):
                    self.assignment = assignment
                    return True
                
                # Progress logging
                if flip % 100 == 0:
                    progress = (current_satisfied / len(self.clauses)) * 100
                    logging.info(f"Try {try_num + 1}, Flip {flip}: {current_satisfied}/{len(self.clauses)} "
                               f"clauses satisfied ({progress:.1f}%)")
                
                if random.random() < h:
                    # Random walk: flip random variable
                    var = random.choice(list(self.variables))
                else:
                    # Greedy selection: try all variables and pick best
                    best_score = -1
                    best_vars = []
                    
                    for var in self.variables:
                        # Calculate score for flipping this variable
                        test_assignment = assignment.copy()
                        test_assignment[var] = not test_assignment[var]
                        score = self.count_satisfied_clauses(test_assignment)
                        
                        if score > best_score:
                            best_score = score
                            best_vars = [var]
                        elif score == best_score:
                            best_vars.append(var)
                    
                    if best_score <= current_satisfied:
                        break
                        
                    var = random.choice(best_vars)
                
                assignment[var] = not assignment[var]
                current_satisfied = self.count_satisfied_clauses(assignment)
                
                if current_satisfied > self.best_satisfied_count:
                    self.best_satisfied_count = current_satisfied
                    self.best_assignment = assignment.copy()

        self.assignment = self.best_assignment
        return False

    def write_solution(self, filename: str) -> None:
        """Write the solution to a file"""
        if not self.assignment:
            raise ValueError("No solution exists")
        
        with open(filename, 'w') as f:
            for var in sorted(self.variables):
                if self.assignment[var]:
                    f.write(f"{var}\n")

    def validate_solution(self) -> bool:
        """Validate that the current assignment satisfies all clauses"""
        for i, clause in enumerate(self.clauses):
            if not self.evaluate_clause(clause, self.assignment):
                logging.warning(f"Clause {i} not satisfied: {clause}")
                return False
        return True