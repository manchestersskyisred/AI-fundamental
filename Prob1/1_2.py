def dijkstra(n, edges):
    grid = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    for x, y, z in edges:
        grid[x][y] = z
    
    dist = [float('inf')] * (n+1)
    dist[1] = 0
    visited = [False] * (n+1)
    
    for _ in range(n):
        min_dist = float('inf')
        min_node = -1
        for i in range(1, n+1):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                min_node = i
        
        if min_node == -1:
            break
        
        visited[min_node] = True
        
        for v in range(1, n+1):
            if not visited[v] and grid[min_node][v] != float('inf') and dist[min_node] + grid[min_node][v] < dist[v]:
                dist[v] = dist[min_node] + grid[min_node][v]
    
    return dist[n] if dist[n] != float('inf') else -1

n, m = map(int, input().split())
edges = []
for _ in range(m):
    x, y, z = map(int, input().split())
    edges.append((x, y, z))

print(dijkstra(n, edges)) 