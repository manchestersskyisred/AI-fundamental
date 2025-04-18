import matplotlib.pyplot as plt
import numpy as np

def visualize_maze_with_path(maze, path, visited):
    plt.figure(figsize=(10, 10))
    maze_array = np.array(maze)
    
    # 绘制迷宫地形
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'lightblue', 'green'])
    bounds = [0, 1, 2, 3, 4]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
    plt.imshow(maze_array, cmap=cmap, norm=norm)
    
    # 标记访问过的节点（浅黄色）
    for (i, j) in visited:
        plt.fill([j-0.5, j+0.5, j+0.5, j-0.5], [i-0.5, i-0.5, i+0.5, i+0.5], color='yellow', alpha=0.3)
    
    # 绘制路径（红色线条）
    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        plt.plot(path_x, path_y, color='red', linewidth=2, marker='o', markersize=8)
    
    # 设置坐标轴和标题
    plt.xticks(range(len(maze[0])))
    plt.yticks(range(len(maze)))
    plt.gca().set_xticks([x - 0.5 for x in range(1, len(maze[0]))], minor=True)
    plt.gca().set_yticks([y - 0.5 for y in range(1, len(maze))], minor=True)
    plt.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
    plt.title("A* Pathfinding Visualization")
    plt.show()