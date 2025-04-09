import sys
import heapq

goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def distance(state):
    dist = 0
    for i in range(9):
        if state[i] == 0:
            continue
        tar_r, tar_c = (state[i]-1) // 3, (state[i]-1) % 3
        cur_r, cur_c = i // 3, i % 3
        dist += ((tar_r - cur_r)**2 + (tar_c - cur_c)**2)**0.5
    return dist

def is_solvable(start):
    inv = 0
    for i in range(9):
        for j in range(i+1, 9):
            if start[j] and start[i] and start[i] > start[j]:
                inv += 1
    return inv % 2 == 0

def next_state(state):
    new_states = []
    pos0 = state.index(0)
    i, j = pos0 // 3, pos0 % 3
    dir = [(-1, 0, 'u'), (1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r')]
    for posi, posj, move in dir:
        new_i, new_j = i + posi, j + posj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_pos = new_i * 3 + new_j
            new_state = list(state)
            new_state[pos0], new_state[new_pos] = new_state[new_pos], new_state[pos0]
            new_states.append((tuple(new_state), move))
    return new_states

def A_star(start, goal):
    if start == goal:
        return 0
    heap = []
    heapq.heappush(heap, (distance(start), 0, start,""))
    visited = {start: 0}
    while heap:
        f, g, state, path = heapq.heappop(heap) 
        if state == goal:
            return path
        for new_state, move in next_state(state):
            new_g = g + 1
            new_f = new_g + distance(new_state)
            if new_state not in visited or visited[new_state] > new_g:
                visited[new_state] = new_g
                heapq.heappush(heap, (new_f, new_g, new_state, path + move))
    return "unsolvable"

def main():
    input_str = sys.stdin.readline().strip().split()
    start = []
    for c in input_str:
        if c == 'x':
            start.append(0)
        else:
            start.append(int(c))
    if not is_solvable(start):
        print("unsolvable")
        return
    start_tuple = tuple(start)
    result = A_star(start_tuple, goal)
    print(result)
if __name__ == "__main__":
    main()