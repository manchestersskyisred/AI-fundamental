import sys
def dijkstra():
    n, m = map(int, sys.stdin.readline().split())
    INF = int(10001)
    g = [(n + 1) * [INF] for _ in range(n + 1)] #邻接矩阵，g[x][y]表示从x到y的边权
    for _ in range(m): #处理每条边，保留最短边权
        x, y, z = map(int, sys.stdin.readline().split())
        if z < g[x][y]: #如果新边更短，则更新
            g[x][y] = z
    dis = (n + 1) * [INF]
    dis[1] = 0
    visited = (n + 1) * [False] #标记节点是否已确定最短路径
    for _ in range(n):
        u = -1
        min_dis = INF
        for i in range(1, n + 1): #找到当前未访问且距离最小的节点u
            if not visited[i] and dis[i] < min_dis:
                min_dis = dis[i]
                u = i
        if u == -1: #没有可达节点待处理
            break
        visited[u] = True #标记u已确定最短路径
        for v in range(1, n + 1): #通过u更新所有邻接节点v的距离
            if g[u][v] != INF and not visited[v]:
                if dis[v] > dis[u] + g[u][v]:
                    dis[v] = dis[u] + g[u][v]
    if dis[n] == INF:
        print(-1)
    else:
        print(dis[n])
if __name__ == "__main__":
    dijkstra()