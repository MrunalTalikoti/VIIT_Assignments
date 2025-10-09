"""
8–Queens Problem – Basic Search Strategies
------------------------------------------

Goal:
Place 8 queens on a chessboard so that no two queens attack each other.

Implemented Search Strategies:
1. Backtracking Search (Depth-First)
2. Breadth-First Search (BFS)
3. Min-Conflicts (Local Search)

Each algorithm is demonstrated, and one valid board configuration is printed.
"""

import random
from collections import deque

# -------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------

def is_safe(positions, col, row):
    """
    Check if placing a queen at (col, row) is safe given the
    existing partial assignment of queens in 'positions'.
    """
    for c, r in enumerate(positions):
        # Same row or same diagonal -> conflict
        if r == row or abs(r - row) == abs(c - col):
            return False
    return True


def print_board(positions):
    """Print the chessboard for a given solution."""
    N = len(positions)
    for r in range(N):
        line = ""
        for c in range(N):
            line += "Q " if positions[c] == r else ". "
        print(line)
    print()


# -------------------------------------------------------------
# 1. Backtracking Search
# -------------------------------------------------------------
def solve_backtracking(N):
    """
    Classic DFS (Depth-First Search) backtracking approach.
    Places one queen per column and backtracks when a conflict arises.
    """
    solutions = []

    def backtrack(col, positions):
        # Base Case: All queens are placed
        if col == N:
            solutions.append(positions.copy())
            return

        # Try placing a queen in each row of the current column
        for row in range(N):
            if is_safe(positions, col, row):
                positions.append(row)
                backtrack(col + 1, positions)
                positions.pop()  # backtrack

    backtrack(0, [])
    return solutions


# -------------------------------------------------------------
# 2. Breadth-First Search
# -------------------------------------------------------------
def solve_bfs(N):
    """
    BFS builds partial solutions level by level (column by column).
    Each node in the queue represents a partial placement of queens.
    """
    queue = deque([[]])  # Start with an empty board
    while queue:
        state = queue.popleft()
        col = len(state)

        # If 8 queens are placed, return the first complete solution
        if col == N:
            return state

        # Try extending the current partial solution
        for row in range(N):
            if is_safe(state, col, row):
                queue.append(state + [row])
    return None


# -------------------------------------------------------------
# 3. Min-Conflicts (Local Search)
# -------------------------------------------------------------
def conflicts_for(positions, col, row):
    """Count number of conflicts if queen at column col is placed in row."""
    count = 0
    for c, r in enumerate(positions):
        if c != col and (r == row or abs(r - row) == abs(c - col)):
            count += 1
    return count


def solve_min_conflicts(N, max_steps=10000, max_restarts=50):
    """
    Local search algorithm:
    - Start with a random configuration.
    - Repeatedly move a conflicted queen to a position with minimum conflicts.
    - Restart if stuck.
    """
    for restart in range(max_restarts):
        positions = [random.randrange(N) for _ in range(N)]

        for step in range(max_steps):
            # Find columns with conflicts
            conflict_cols = [c for c in range(N) if conflicts_for(positions, c, positions[c]) > 0]

            if not conflict_cols:
                # Solution found
                return positions

            # Choose a random conflicted column
            col = random.choice(conflict_cols)

            # Find row with minimum conflict in that column
            conflict_counts = [conflicts_for(positions, col, r) for r in range(N)]
            min_conflict = min(conflict_counts)
            best_rows = [r for r, val in enumerate(conflict_counts) if val == min_conflict]

            # Move queen to the best row (break ties randomly)
            positions[col] = random.choice(best_rows)
    return None


# -------------------------------------------------------------
# MAIN PROGRAM EXECUTION
# -------------------------------------------------------------
if __name__ == "__main__":
    N = 8  # Board size

    print("====== 8-Queens Problem ======\n")

    # --- 1. Backtracking ---
    print("1. Backtracking Search:")
    bt_solutions = solve_backtracking(N)
    print(f"Total Solutions Found: {len(bt_solutions)}\n")
    print("Sample Solution:")
    print_board(bt_solutions[0])

    # --- 2. Breadth-First Search ---
    print("2. Breadth-First Search:")
    bfs_solution = solve_bfs(N)
    if bfs_solution:
        print("Solution Found:")
        print_board(bfs_solution)
    else:
        print("No Solution Found.\n")

    # --- 3. Min-Conflicts (Local Search) ---
    print("3. Min-Conflicts (Local Search):")
    mc_solution = solve_min_conflicts(N)
    if mc_solution:
        print("Solution Found:")
        print_board(mc_solution)
    else:
        print("Failed to find solution using Min-Conflicts.\n")
