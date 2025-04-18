import sys
def dijkstra():
    n, m = map(int, sys.stdin.readline().split())
    INF = int(10001)
    g = [(n + 1) * [INF] for _ in range(n + 1)] 
    for _ in range(m): 
        x, y, z = map(int, sys.stdin.readline().split())
        if z < g[x][y]: 
            g[x][y] = z
    dis = (n + 1) * [INF]
    dis[1] = 0
    visited = (n + 1) * [False] 
    for _ in range(n):
        u = -1
        min_dis = INF
        for i in range(1, n + 1): 
            if not visited[i] and dis[i] < min_dis:
                min_dis = dis[i]
                u = i
        if u == -1: 
            break
        visited[u] = True 
        for v in range(1, n + 1): 
            if g[u][v] != INF and not visited[v]:
                if dis[v] > dis[u] + g[u][v]:
                    dis[v] = dis[u] + g[u][v]
    if dis[n] == INF:
        print(-1)
    else:
        print(dis[n])
if __name__ == "__main__":
    dijkstra()