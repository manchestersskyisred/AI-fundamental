import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# --- Colors --- 
TERRAIN_COLORS = {
    0: [0.2, 0.2, 0.2],  # Wall (Dark Gray)
    1: [1.0, 1.0, 1.0],  # Road (White)
    2: [0.5, 0.8, 1.0],  # Highway (Light Blue)
    3: [0.8, 0.5, 0.2],  # Mud (Brown)
    4: [1.0, 0.85, 0.0], # Treasure (Gold)
}
OPEN_COLOR = [0.6, 1.0, 0.6] # Light Green
CLOSED_COLOR = [0.9, 0.9, 0.9] # Light Gray
CURRENT_COLOR = [1.0, 0.5, 0.0] # Orange
START_COLOR = 'lime'
GOAL_COLOR = 'purple' # Default, will be gold if goal is treasure
PATH_COLOR = 'green' # Color for final path overlay

def visualize_maze_step(ax, maze, current, open_set, closed_set, start, goal):
    """
    Draws a single step of the A* search onto the provided axes.
    """
    rows, cols = len(maze), len(maze[0])
    colored_maze = np.zeros((rows, cols, 3))
    
    # 1. Base terrain colors
    for r in range(rows):
        for c in range(cols):
            cell_type = maze[r][c]
            colored_maze[r, c] = TERRAIN_COLORS.get(cell_type, [0,0,0])
            
    # 2. Closed set (visited)
    for r, c in closed_set:
        if (r, c) != start and (r, c) != goal: # Don't overwrite start/goal base color yet
             if maze[r][c] != 4: # Don't overwrite treasure
                 colored_maze[r, c] = CLOSED_COLOR
            
    # 3. Open set (frontier)
    for r, c in open_set:
        if (r, c) != start and (r, c) != goal:
            if maze[r][c] != 4:
                 colored_maze[r, c] = OPEN_COLOR
            
    # 4. Current node being processed
    if current:
        r, c = current
        if (r, c) != start and (r, c) != goal:
             if maze[r][c] != 4:
                 colored_maze[r, c] = CURRENT_COLOR
                 
    # 5. Start and Goal Markers (override colors)
    start_r, start_c = start
    goal_r, goal_c = goal
    colored_maze[start_r, start_c] = TERRAIN_COLORS.get(maze[start_r][start_c], [1,1,1]) # Ensure start terrain visible
    if maze[goal_r][goal_c] == 4:
        colored_maze[goal_r, goal_c] = TERRAIN_COLORS[4] # Ensure goal terrain visible if treasure
        goal_marker_color = TERRAIN_COLORS[4]
    else:
         colored_maze[goal_r, goal_c] = TERRAIN_COLORS.get(maze[goal_r][goal_c], [1,1,1])
         goal_marker_color = GOAL_COLOR

    ax.imshow(colored_maze, interpolation='nearest')

    # Mark start and goal explicitly
    ax.plot(start_c, start_r, marker='*', markersize=15, color=START_COLOR, linestyle='None')
    ax.plot(goal_c, goal_r, marker='X', markersize=15, color=goal_marker_color, linestyle='None')

    # Setup Grid and Ticks
    ax.set_xticks(np.arange(cols))
    ax.set_yticks(np.arange(rows))
    ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
    ax.tick_params(which='minor', size=0)
    ax.tick_params(axis='both', which='major', labelsize=8, bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False) # Hide ticks and labels
    
    # Add Legend (Simplified for animation)
    legend_elements = [
        mpatches.Patch(color=OPEN_COLOR, label='Open Set'),
        mpatches.Patch(color=CLOSED_COLOR, label='Closed Set'),
        mpatches.Patch(color=CURRENT_COLOR, label='Current'),
        mpatches.Patch(color=START_COLOR, label='Start'),
        mpatches.Patch(color=goal_marker_color, label='Goal')
    ]
    # Clear previous legends if any
    if ax.legend_:
        ax.legend_.remove()
    ax.legend(handles=legend_elements, loc='upper center', 
              bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize='x-small')

# Renamed original function for potentially drawing final state separately if needed
def visualize_maze_final(ax, maze, path, visited=None):
    """
    Visualizes the final maze state with the path.
    (Based on the original visualize_maze_with_path)
    """
    rows, cols = len(maze), len(maze[0])
    colored_maze = np.zeros((rows, cols, 3))

    # Define colors (could reuse from top, but keep self-contained for now)
    colors = TERRAIN_COLORS
    visited_color = CLOSED_COLOR # Use closed color for visited
    path_color = [1.0, 0.6, 0.6] # Original path color (Light Red)
    start_marker_color = START_COLOR
    end_marker_color = GOAL_COLOR

    # Set base terrain colors
    for i in range(rows):
        for j in range(cols):
            cell_type = maze[i][j]
            colored_maze[i, j] = colors.get(cell_type, [0.0, 0.0, 0.0])

    # Color visited cells (excluding path)
    if visited:
        path_set = set(path) if path else set()
        for i, j in visited:
            if (i, j) not in path_set:
                if maze[i][j] != 4 and maze[i][j] != 0:
                     colored_maze[i, j] = visited_color

    # Color the final path
    if path:
        for i, j in path:
             if maze[i][j] != 4 or (i,j) != path[-1]: # Don't overwrite goal treasure color
                 colored_maze[i, j] = path_color
        # Ensure goal is its terrain color if treasure
        goal_r, goal_c = path[-1]
        if maze[goal_r][goal_c] == 4:
             colored_maze[goal_r, goal_c] = colors[4]
             end_marker_color = colors[4]
        else:
             # Recolor end of path if not treasure
             colored_maze[goal_r, goal_c] = path_color
             
    ax.imshow(colored_maze, interpolation='nearest')

    # Draw path line
    if path:
        y, x = zip(*path)
        ax.plot(x, y, color=PATH_COLOR, linestyle='-', linewidth=3, label='Final Path')

        # Mark start and end
        ax.plot(path[0][1], path[0][0], marker='*', markersize=15, color=start_marker_color, linestyle='None')
        ax.plot(path[-1][1], path[-1][0], marker='X', markersize=15, color=end_marker_color, linestyle='None')

    # Setup Grid and Ticks
    ax.set_xticks(np.arange(cols))
    ax.set_yticks(np.arange(rows))
    ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
    ax.tick_params(which='minor', size=0)
    ax.tick_params(axis='both', which='major', labelsize=8)

    # Add Legend for final state
    legend_elements = [
        mpatches.Patch(color=colors[0], label='Wall'),
        mpatches.Patch(color=colors[1], label='Road'),
        mpatches.Patch(color=colors[2], label='Highway'),
        mpatches.Patch(color=colors[3], label='Mud'),
        mpatches.Patch(color=colors[4], label='Treasure'),
        mpatches.Patch(color=visited_color, label='Visited'),
        mpatches.Patch(color=path_color, label='Path Cells'),
        mpatches.Patch(color=PATH_COLOR, label='Final Path Line'),
        mpatches.Patch(color=start_marker_color, label='Start'),
        mpatches.Patch(color=end_marker_color, label='End')
    ]
    if ax.legend_:
        ax.legend_.remove()
    ax.legend(handles=legend_elements, loc='upper center',
               bbox_to_anchor=(0.5, -0.08), ncol=4, fontsize='x-small')

    ax.set_title('A* Maze - Final Path')
    # Don't call plt.tight_layout() or plt.show() here

    plt.figure(figsize=(max(8, cols * 0.6), max(8, rows * 0.6))) # Adjusted figsize
    plt.imshow(colored_maze, interpolation='nearest')

    # 绘制路径线
    if path:
        y, x = zip(*path)
        plt.plot(x, y, 'r-', linewidth=2)  # 红色线
        # plt.plot(x, y, 'ro', markersize=4)  # Optional: smaller red dots

        # 标记起点和终点
        plt.plot(path[0][1], path[0][0], marker='*', markersize=15, color='lime') # Brighter green
        end_marker_color = colors[4] if maze[path[-1][0]][path[-1][1]] == 4 else 'purple'
        plt.plot(path[-1][1], path[-1][0], marker='X', markersize=15, color=end_marker_color)

    # 设置坐标轴刻度和边框
    plt.xticks(np.arange(cols))
    plt.yticks(np.arange(rows))
    plt.gca().set_xticks(np.arange(-.5, cols, 1), minor=True)
    plt.gca().set_yticks(np.arange(-.5, rows, 1), minor=True)
    plt.grid(which="minor", color="black", linestyle='-', linewidth=1)
    plt.tick_params(which='minor', size=0) # Hide minor ticks
    plt.tick_params(axis='both', which='major', labelsize=8) # Smaller axis labels


    # 添加图例
    legend_elements = [
        mpatches.Patch(color=colors[0], label='Wall (0)'),
        mpatches.Patch(color=colors[1], label='Road (1)'),
        mpatches.Patch(color=colors[2], label='Highway (2)'),
        mpatches.Patch(color=colors[3], label='Mud (3)'),
        mpatches.Patch(color=colors[4], label='Treasure (4)'),
        mpatches.Patch(color=visited_color, label='Visited Cells'),
        mpatches.Patch(color=path_color, label='Final Path'),
        mpatches.Patch(color='lime', label='Start'),
        mpatches.Patch(color=end_marker_color, label='End')
    ]
    plt.legend(handles=legend_elements, loc='upper center',
               bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize='small') # Adjusted legend position and size

    plt.title('A* Maze Path Visualization')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
    plt.show() 