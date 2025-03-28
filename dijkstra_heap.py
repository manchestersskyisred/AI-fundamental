import heapq

def dijkstra_heap(n, edges):
    graph = [[] for _ in range(n+1)]
    for x, y, z in edges:
        graph[x].append((y, z))  
    
    dist = [float('inf')] * (n+1)
    dist[1] = 0
    
    pq = [(0, 1)]  
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_dist > dist[curr_node]:
            continue
        
        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return dist[n] if dist[n] != float('inf') else -1

n, m = map(int, input().split())
edges = []
for _ in range(m):
    x, y, z = map(int, input().split())
    edges.append((x, y, z))

print(dijkstra_heap(n, edges)) 