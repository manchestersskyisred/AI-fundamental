from collections import deque
goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def generate_new_states(state):
    new_states = []
    pos0 = state.index(0)
    i, j = pos0 // 3, pos0 % 3
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in dir:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_pos = ni * 3 + nj
            new_state = list(state)
            new_state[pos0], new_state[new_pos] = new_state[new_pos], new_state[pos0]
            new_states.append(tuple(new_state))
    return new_states

def dfs(state, cnt=0):
    if state == goal:
        return cnt 
    visited_states = set() #记录已访问的状态
    q = deque([(state, cnt)]) #队列，存储当前状态和深度
    while q:
        state, cnt = q.popleft()
        if state in visited_states:
            continue 
        visited_states.add(state)
        for new_state in generate_new_states(state): #遍历所有可能的新状态
            if new_state == goal:
                return cnt + 1  # 如果新状态是目标状态，返回深度+1
            q.append((new_state, cnt + 1))  # 将新状态加入队列
    return -1
def main():
    input_str = input().strip().split()
    state = []
    for c in input_str:
        if c == 'x':
            state.append(0)
        elif c.isdigit():
            state.append(int(c))
    result = dfs(tuple(state))
    if result == -1:
        print(0)
    else:
        print(1)
if __name__ == "__main__":
    main()