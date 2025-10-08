from collections import deque
import copy

# Goal state
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# Moves: up, down, left, right
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_blank_pos(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def generate_neighbors(state):
    x, y = get_blank_pos(state)
    neighbors = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def bfs(start_state):
    visited = set()
    queue = deque([(start_state, [])])
    visited.add(state_to_tuple(start_state))

    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            return path + [state]

        for neighbor in generate_neighbors(state):
            t = state_to_tuple(neighbor)
            if t not in visited:
                visited.add(t)
                queue.append((neighbor, path + [state]))
    return None


def dfs(start_state, depth_limit=50):
    visited = set()

    def dfs_recursive(state, path, depth):
        if state == goal_state:
            return path + [state]
        if depth >= depth_limit:
            return None

        visited.add(state_to_tuple(state))
        for neighbor in generate_neighbors(state):
            t = state_to_tuple(neighbor)
            if t not in visited:
                result = dfs_recursive(neighbor, path + [state], depth + 1)
                if result:
                    return result
        return None

    return dfs_recursive(start_state, [], 0)


def print_solution(solution):
    if not solution:
        print("No solution found.")
        return
    print(f"\nSolution found in {len(solution) - 1} moves:")
    for step in solution:
        for row in step:
            print(row)
        print("----")


def input_state():
    print("Enter the puzzle state row by row (use 0 for blank):")
    state = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        if len(row) != 3:
            raise ValueError("Each row must have exactly 3 numbers.")
        state.append(row)
    return state


# ------------------------------
# Main Menu
# ------------------------------
if __name__ == "__main__":
    while True:
        print("\n--- 8 Puzzle Solver ---")
        print("1. Solve using BFS")
        print("2. Solve using DFS")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            start = input_state()
            print("\nSolving with BFS...")
            solution = bfs(start)
            print_solution(solution)

        elif choice == "2":
            start = input_state()
            print("\nSolving with DFS...")
            solution = dfs(start, depth_limit=50)
            print_solution(solution)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please try again.")
explain the entire code and also give me theorotical

