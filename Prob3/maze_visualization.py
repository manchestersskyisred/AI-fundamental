"""
迷宫可视化模块：对搜索过的格子染色
"""
import matplotlib.pyplot as plt
import numpy as np

def visualize_maze_with_path(maze, path, visited=None):
    """
    可视化迷宫、搜索路径和访问过的格子
    
    Args:
        maze: 二维数组表示的迷宫，0表示可通过的路，1表示不可通过的墙壁
        path: 最终路径的格子坐标列表，如[(0,0), (1,0), ...]
        visited: 所有被搜索过的格子坐标集合
    """
    # 创建一个彩色迷宫数组用于可视化
    rows, cols = len(maze), len(maze[0])
    colored_maze = np.zeros((rows, cols, 3))
    
    # 设置基础颜色：白色为通道，灰色为墙壁
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:  # 墙壁
                colored_maze[i, j] = [0.7, 0.7, 0.7]  # 灰色
            else:  # 通道
                colored_maze[i, j] = [1.0, 1.0, 1.0]  # 白色
    
    # 为访问过的格子染色（浅蓝色）
    if visited:
        for i, j in visited:
            if (i, j) not in path:  # 不包括最终路径上的格子
                colored_maze[i, j] = [0.7, 0.9, 1.0]  # 浅蓝色
    
    # 为路径染色（红色）
    if path:
        for i, j in path:
            colored_maze[i, j] = [1.0, 0.6, 0.6]  # 浅红色
    
    plt.figure(figsize=(10, 10 * rows / cols))
    plt.imshow(colored_maze, interpolation='nearest')
    
    # 绘制路径线
    if path:
        y, x = zip(*path)
        plt.plot(x, y, 'r-', linewidth=2)  # 红色线
        plt.plot(x, y, 'ro', markersize=6)  # 红色点
        
        # 标记起点和终点
        plt.plot(path[0][1], path[0][0], marker='*', markersize=15, color='green')
        plt.plot(path[-1][1], path[-1][0], marker='X', markersize=15, color='purple')
    
    # 设置坐标轴刻度和边框
    plt.xticks(range(cols))
    plt.yticks(range(rows))
    plt.gca().set_xticks([x - 0.5 for x in range(1, cols)], minor=True)
    plt.gca().set_yticks([y - 0.5 for y in range(1, rows)], minor=True)
    plt.grid(which="minor", color="black", linestyle='-', linewidth=1)
    
    # 添加图例
    import matplotlib.patches as mpatches
    legend_elements = [
        mpatches.Patch(color=[0.7, 0.7, 0.7], label='Wall'),
        mpatches.Patch(color=[1.0, 1.0, 1.0], label='Path'),
        mpatches.Patch(color=[0.7, 0.9, 1.0], label='Visited Cells'),
        mpatches.Patch(color=[1.0, 0.6, 0.6], label='Final Path'),
        mpatches.Patch(color='green', label='Start'),
        mpatches.Patch(color='purple', label='End')
    ]
    plt.legend(handles=legend_elements, loc='upper center', 
               bbox_to_anchor=(0.5, -0.05), ncol=3)
    
    plt.title('Maze Path Visualization')
    plt.tight_layout()
    plt.show()