from maze_visualization import visualize_maze_with_path

def dfs(maze):
    rows, cols = len(maze), len(maze[0])
    
    start = (0, 0)  # 左上角
    end = (rows-1, cols-1)  # 右下角
    
    if maze[0][0] == 1 or maze[rows-1][cols-1] == 1:
        return None, set()
    
    visited = set()
    path = []
    parent = {start: None}
    
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def dfs(current):
        nonlocal path
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return True
        
        visited.add(current)
        
        for dx, dy in directions:
            next_x, next_y = current[0] + dx, current[1] + dy
            next_cell = (next_x, next_y)
            
            if (0 <= next_x < rows and 0 <= next_y < cols and 
                maze[next_x][next_y] == 0 and next_cell not in visited):
                parent[next_cell] = current
                if dfs(next_cell):
                    return True
        
        return False
    
    if dfs(start):
        return path, visited
    else:
        return None, visited

if __name__ == "__main__":
    n, m = map(int, input().strip().split())
    maze = []
    for _ in range(n):
        row = list(map(int, input().strip().split()))
        maze.append(row)
    
    path, visited = dfs(maze)
    
    if path:
        print(len(path) - 1)  
        visualize_maze_with_path(maze, path, visited)
    else:
        print("无法到达终点") 