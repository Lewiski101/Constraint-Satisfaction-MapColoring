class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

    def is_consistent(self, var, value, assignment):
        """Checks if assigning value to var is consistent with existing assignment."""
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment and not self.constraints(var, value, neighbor, assignment[neighbor]):
                return False
        return True

    def backtracking_search(self):
        return self._backtrack({})

    def _backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        # Select unassigned variable (using MRV - Minimum Remaining Values)
        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.domains[v]))

        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self._backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

def map_coloring_constraints(v1, c1, v2, c2):
    """Basic map coloring constraint: adjacent regions must have different colors."""
    return c1 != c2
