from collections import deque
from maze_visualization import visualize_maze_with_path

def bfs(maze):
    rows, cols = len(maze), len(maze[0])
    start = (0, 0)  
    end = (rows-1, cols-1) 
    
    queue = deque([start])
    visited = set([start])  
    parent = {start: None}  
    
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()  
            return path, visited
        
        for dx, dy in directions:
            next_x, next_y = current[0] + dx, current[1] + dy
            next_cell = (next_x, next_y)
            
            if (0 <= next_x < rows and 0 <= next_y < cols and 
                maze[next_x][next_y] == 0 and next_cell not in visited):
                queue.append(next_cell)
                visited.add(next_cell)
                parent[next_cell] = current
    
    return None, visited

if __name__ == "__main__":
    n, m = map(int, input().strip().split())
    maze = []
    for _ in range(n):
        row = list(map(int, input().strip().split()))
        maze.append(row)
    
    path, visited = bfs(maze)
    
    if path:
        print(len(path) - 1)  
        visualize_maze_with_path(maze, path, visited)
    else:
        print("无法到达终点")
            