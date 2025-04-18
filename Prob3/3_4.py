
import heapq
from maze_visualization import visualize_maze_with_path

def heuristic(position, goal):
    return ((position[0] - goal[0])**2 + (position[1] - goal[1])**2)**0.5

def next_positions(maze, position):

    rows, cols = len(maze), len(maze[0])
    row, col = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
    neighbors = []
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < rows and 0 <= new_col < cols and 
            maze[new_row][new_col] == 0):
            neighbors.append((new_row, new_col))
    
    return neighbors

def a_star(maze):
    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    goal = (rows-1, cols-1)
    
    if maze[0][0] == 1 or maze[rows-1][cols-1] == 1:
        return None, set()
    
    heap = [(heuristic(start, goal), 0, start)]
    g_scores = {start: 0}  
    visited = set()
    parent = {start: None}
    
    while heap:
        f, g, position = heapq.heappop(heap)
        
        if position in visited:
            continue
        
        visited.add(position)
        
        if position == goal:
            path = []
            current = position
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, visited
        
        for next_pos in next_positions(maze, position):
            new_g = g + 1
            
            if next_pos not in g_scores or new_g < g_scores[next_pos]:
                g_scores[next_pos] = new_g
                f = new_g + heuristic(next_pos, goal)
                parent[next_pos] = position
                heapq.heappush(heap, (f, new_g, next_pos))
    
    return None, visited

if __name__ == "__main__":
    n, m = map(int, input().strip().split())
    maze = []
    for _ in range(n):
        row = list(map(int, input().strip().split()))
        maze.append(row)
    
    path, visited = a_star(maze)
    
    if path:
        print(len(path) - 1)  # 移动次数是路径长度减1
        visualize_maze_with_path(maze, path, visited)
    else:
        print("无法到达终点")
