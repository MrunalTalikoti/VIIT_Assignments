from collections import deque
import heapq

# Goal state
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Neighbor generation (moves)
def neighbors(state):
    idx = state.index(0)
    x, y = divmod(idx, 3)
    result = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            nidx = nx*3 + ny
            lst = list(state)
            lst[idx], lst[nidx] = lst[nidx], lst[idx]
            result.append(tuple(lst))
    return result

# BFS Algorithm
def bfs(start):
    if start == GOAL:
        return [start]
    queue = deque([start])
    visited = {start}
    parent = {}
    while queue:
        state = queue.popleft()
        for n in neighbors(state):
            if n not in visited:
                visited.add(n)
                parent[n] = state
                if n == GOAL:
                    path = [n]
                    while path[-1] != start:
                        path.append(parent[path[-1]])
                    return list(reversed(path))
                queue.append(n)
    return None

# A* Algorithm (with Manhattan heuristic)
def manhattan(state):
    dist = 0
    for i, v in enumerate(state):
        if v == 0: continue
        goal_idx = GOAL.index(v)
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_idx, 3)
        dist += abs(x1 - x2) + abs(y1 - y2)
    return dist

def a_star(start):
    open_heap = []
    heapq.heappush(open_heap, (manhattan(start), start))
    g = {start: 0}
    parent = {}
    visited = set()
    while open_heap:
        _, state = heapq.heappop(open_heap)
        if state == GOAL:
            path = [state]
            while path[-1] in parent:
                path.append(parent[path[-1]])
            return list(reversed(path))
        visited.add(state)
        for n in neighbors(state):
            tentative_g = g[state] + 1
            if n not in visited or tentative_g < g.get(n, float('inf')):
                parent[n] = state
                g[n] = tentative_g
                heapq.heappush(open_heap, (tentative_g + manhattan(n), n))
    return None

# ---------------------------
# Simple Example (Solvable)
# ---------------------------
start_state = (1, 2, 3, 4, 5, 6, 7, 0, 8)

print("Start state:")
for i in range(0, 9, 3):
    print(start_state[i:i+3])

print("\nGoal state:")
for i in range(0, 9, 3):
    print(GOAL[i:i+3])

# Run BFS
bfs_path = bfs(start_state)
print("\nBFS Path:")
for step in bfs_path:
    for i in range(0, 9, 3):
        print(step[i:i+3])
    print()

# Run A*
a_path = a_star(start_state)
print("A* Path:")
for step in a_path:
    for i in range(0, 9, 3):
        print(step[i:i+3])
    print()

