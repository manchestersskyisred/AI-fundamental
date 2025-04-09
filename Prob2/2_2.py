from collections import deque
import sys

goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def next_state(state):
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    new_states = []
    pos0 = state.index(0)
    i,j = pos0 // 3, pos0 % 3
    for posi,posj in dir:
        new_i,new_j = i + posi, j + posj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = list(state)
            new_state[pos0],new_state[new_i*3+new_j] = new_state[new_i*3+new_j],new_state[pos0]
            new_states.append(tuple(new_state))
    return new_states
    
def bfs(start, goal):
    if start == goal:
        return 0
    queue = deque()
    queue.append((start, 0))
    visited = set()
    visited.add(start)
    while queue:
        current_state, steps = queue.popleft()
        for new_state in next_state(current_state):
            if new_state == goal:
                return steps + 1
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + 1))
    return -1

def main():
    input_str = sys.stdin.readline().strip().split()
    start = []
    for i in input_str:
        if i == 'x':
            start.append(0)
        else:
            start.append(int(i))
    start_tuple = tuple(start)
    result = bfs(start_tuple, goal)
    print(result)
if __name__ == "__main__":
    main()