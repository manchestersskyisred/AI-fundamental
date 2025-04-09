import heapq
from maze_visualization import visualize_maze_with_path

def dijkstra(maze):
    rows, cols = len(maze), len(maze[0])
    
    start = (0, 0)  
    end = (rows-1, cols-1)  
    
    if maze[0][0] == 1 or maze[rows-1][cols-1] == 1:
        return None, set()
    
    pq = [(0, start)]  
    distances = {start: 0}
    visited = set()
    parent = {start: None}
    
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while pq:
        dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, visited
        
        for dx, dy in directions:
            next_x, next_y = current[0] + dx, current[1] + dy
            next_cell = (next_x, next_y)
            
            if (0 <= next_x < rows and 0 <= next_y < cols and 
                maze[next_x][next_y] == 0):
                
                new_dist = dist + 1  # 每步距离为1
                if new_dist < distances.get(next_cell, float('inf')):
                    distances[next_cell] = new_dist
                    parent[next_cell] = current
                    heapq.heappush(pq, (new_dist, next_cell))
    
    return None, visited

if __name__ == "__main__":
    n, m = map(int, input().strip().split())
    maze = []
    for _ in range(n):
        row = list(map(int, input().strip().split()))
        maze.append(row)
    
    path, visited = dijkstra(maze)
    
    if path:
        print(len(path) - 1)  
        visualize_maze_with_path(maze, path, visited)
    else:
        print("无法到达终点") 