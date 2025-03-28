from collections import deque

def bfs(n, edges):
    graph = [[] for _ in range(n+1)]
    for u, v in edges:
        graph[u].append(v)
    
    distance = [-1] * (n+1)
    distance[1] = 0
    
    queue = deque([1])
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    return distance[n] if distance[n] != -1 else -1

n, m = map(int, input().split())
edges = []
for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u, v))

print(bfs(n, edges)) 