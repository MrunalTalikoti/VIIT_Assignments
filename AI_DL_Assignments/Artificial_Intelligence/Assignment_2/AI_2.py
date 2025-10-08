# menu_csp_solver.py

from collections import defaultdict, deque
import copy

# ------------------ CSP Framework ------------------

class CSP:
    def __init__(self, variables, domains):
        self.variables = list(variables)
        self.domains = {v: list(domains[v]) for v in self.variables}
        self.constraints = defaultdict(list)
        self.neighbors = defaultdict(set)

    def add_constraint(self, xi, xj, constraint_fn):
        self.constraints[xi].append((xj, constraint_fn))
        self.constraints[xj].append((xi, lambda y, x: constraint_fn(x, y)))
        self.neighbors[xi].add(xj)
        self.neighbors[xj].add(xi)

    def is_consistent(self, var, assignment):
        val = assignment[var]
        for (nbr, fn) in self.constraints[var]:
            if nbr in assignment and not fn(val, assignment[nbr]):
                return False
        return True

# ------------------ Inference: AC-3 ------------------

def ac3(csp, queue=None):
    if queue is None:
        queue = deque((xi, xj) for xi in csp.variables for (xj, _) in csp.constraints[xi])

    while queue:
        xi, xj = queue.popleft()
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj):
    revised = False
    fns = [fn for (nbr, fn) in csp.constraints[xi] if nbr == xj]
    new_domain = []
    for vi in csp.domains[xi]:
        if any(all(fn(vi, vj) for fn in fns) for vj in csp.domains[xj]):
            new_domain.append(vi)
        else:
            revised = True
    if revised:
        csp.domains[xi] = new_domain
    return revised

# ------------------ Heuristics ------------------

def select_unassigned_variable(assignment, csp):
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(unassigned, key=lambda v: (len(csp.domains[v]), -len(csp.neighbors[v])))

def order_domain_values(var, assignment, csp):
    counts = []
    for val in csp.domains[var]:
        count = 0
        for nbr in csp.neighbors[var]:
            if nbr in assignment: continue
            fns = [fn for (n, fn) in csp.constraints[var] if n == nbr]
            for val2 in csp.domains[nbr]:
                if not all(fn(val, val2) for fn in fns):
                    count += 1
        counts.append((count, val))
    counts.sort()
    return [val for (_, val) in counts]

# ------------------ Backtracking ------------------

def backtracking_search(csp):
    csp = copy.deepcopy(csp)
    if not ac3(csp):  # preprocess
        return None

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            assignment[var] = value
            if csp.is_consistent(var, assignment):
                saved_domains = {v: list(csp.domains[v]) for v in csp.variables}
                csp.domains[var] = [value]
                if ac3(csp, deque((nbr, var) for nbr in csp.neighbors[var])):
                    result = backtrack(assignment)
                    if result: return result
                csp.domains = saved_domains
            del assignment[var]
        return None

    return backtrack({})

# ------------------ Example Problems ------------------

def australia_map_coloring():
    vars = ['WA','NT','SA','Q','NSW','V','T']
    colors = ['red','green','blue']
    domains = {v: colors for v in vars}
    csp = CSP(vars, domains)
    edges = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),
             ('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),('NSW','V')]
    for a,b in edges:
        csp.add_constraint(a,b, lambda x,y: x!=y)
    sol = backtracking_search(csp)
    print("Australia Map Coloring Solution:", sol)

def sudoku():
    puzzle = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]

    vars, domains = [], {}
    for r in range(9):
        for c in range(9):
            name = f'r{r}c{c}'
            vars.append(name)
            domains[name] = [puzzle[r][c]] if puzzle[r][c] != 0 else list(range(1,10))
    csp = CSP(vars, domains)

    def neq(a,b): return a != b
    for r in range(9):
        for c1 in range(9):
            for c2 in range(c1+1,9):
                csp.add_constraint(f'r{r}c{c1}', f'r{r}c{c2}', neq)
    for c in range(9):
        for r1 in range(9):
            for r2 in range(r1+1,9):
                csp.add_constraint(f'r{r1}c{c}', f'r{r2}c{c}', neq)
    for br in range(3):
        for bc in range(3):
            cells = [(br*3+dr, bc*3+dc) for dr in range(3) for dc in range(3)]
            for i in range(9):
                for j in range(i+1,9):
                    r1,c1 = cells[i]; r2,c2 = cells[j]
                    csp.add_constraint(f'r{r1}c{c1}', f'r{r2}c{c2}', neq)

    sol = backtracking_search(csp)
    print("Sudoku Solution:")
    if sol:
        for r in range(9):
            print(" ".join(str(sol[f'r{r}c{c}']) for c in range(9)))
    else:
        print("No solution found.")

# ------------------ Menu ------------------

def main():
    while True:
        print("\n--- Constraint Satisfaction Problem Solver ---")
        print("1. Solve Australia Map Coloring")
        print("2. Solve Sudoku")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            australia_map_coloring()
        elif choice == "2":
            sudoku()
        elif choice == "3":
            print("Exiting..."); break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
explain the code and give me throutical explanation

