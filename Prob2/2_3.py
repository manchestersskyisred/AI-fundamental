import sys
import heapq


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

def dijkstra(start, goal):
    if start == goal:
        return 0
    heap = []
    heapq.heappush(heap, (0, start))
    dist = {start: 0}
    while heap:
        f, state = heapq.heappop(heap)
        if state == goal:
            return f
        for new_state in next_state(state):
            new_f = f + 1
            if new_state not in dist or dist[new_state] > new_f:
                dist[new_state] = new_f
                heapq.heappush(heap, (new_f, new_state))
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
    result = dijkstra(start_tuple, goal)
    print(result)
if __name__ == "__main__":
    main()