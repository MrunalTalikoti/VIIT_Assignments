# a_star_menu.py

import heapq

# ----------------- A* Algorithm -----------------
def a_star_search(start, goal, neighbors_fn, heuristic_fn):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic_fn(start, goal), 0, start, [start]))
    closed_set = set()

    while open_list:
        f, g, node, path = heapq.heappop(open_list)

        if node == goal:
            return path, g

        if node in closed_set:
            continue
        closed_set.add(node)

        for (neighbor, cost) in neighbors_fn(node):
            if neighbor in closed_set:
                continue
            g_new = g + cost
            f_new = g_new + heuristic_fn(neighbor, goal)
            heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))
    return None, float("inf")

# ----------------- Application 1: Shortest Path in Graph -----------------
graph = {
    "A": [("B", 1), ("C", 3)],
    "B": [("D", 3), ("E", 1)],
    "C": [("F", 5)],
    "D": [("G", 2)],
    "E": [("G", 2)],
    "F": [("G", 1)],
    "G": []
}

def neighbors_graph(node):
    return graph.get(node, [])

def heuristic_graph(node, goal):
    # simple heuristic (straight-line estimate)
    h = {"A": 7, "B": 6, "C": 4, "D": 2, "E": 1, "F": 2, "G": 0}
    return h[node]

def graph_demo():
    print("\n--- A* Search on Graph ---")
    start, goal = "A", "G"
    path, cost = a_star_search(start, goal, neighbors_graph, heuristic_graph)
    print(f"Path from {start} to {goal}: {path}, Cost = {cost}")

# ----------------- Application 2: 8-Puzzle Problem -----------------
goal_state = [[1,2,3],[4,5,6],[7,8,0]]  # 0 represents blank

def neighbors_puzzle(state):
    neighbors = []
    n = 3
    # locate blank
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                x, y = i, j
    # possible moves
    moves = [(0,1),(1,0),(0,-1),(-1,0)]
    for dx,dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < n and 0 <= ny < n:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append((new_state, 1))  # cost = 1 per move
    return neighbors

def heuristic_puzzle(state, goal):
    # Manhattan distance
    dist = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                gi, gj = [(r,c) for r in range(3) for c in range(3) if goal[r][c]==val][0]
                dist += abs(i-gi) + abs(j-gj)
    return dist

def puzzle_demo():
    print("\n--- A* Search on 8-Puzzle ---")
    start_state = [[1,2,3],[4,0,6],[7,5,8]]
    path, cost = a_star_search(start_state, goal_state, neighbors_puzzle, heuristic_puzzle)
    print(f"Solution found in {cost} moves")
    print("Final State:")
    for row in goal_state:
        print(row)

# ----------------- Menu -----------------
def main():
    while True:
        print("\n--- A* Algorithm Applications ---")
        print("1. Shortest Path in Graph")
        print("2. Solve 8-Puzzle Problem")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            graph_demo()
        elif choice == "2":
            puzzle_demo()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
explain entire code step by step and also therotically


