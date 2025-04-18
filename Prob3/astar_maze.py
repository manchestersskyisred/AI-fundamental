import heapq
import numpy as np
from maze_visualization_astar import visualize_maze_step, visualize_maze_final
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches

COSTS = {
    0: float('inf'), 
    1: 1.0,          
    2: 0.5,          
    3: 3.0,           
    4: -1.0        
}

class Node:
    """Represents a node in the search graph"""
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g 
        self.h = h  
        self.f = g + h  

    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        return self.h < other.h

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

def heuristic(a, b):
    """Calculates the Manhattan distance between two points"""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def get_cost(maze, position):
    """Gets the base movement cost for a given cell type, excluding special goal costs."""
    r, c = position
    if 0 <= r < len(maze) and 0 <= c < len(maze[0]):
        cell_type = maze[r][c]
        return COSTS.get(cell_type, float('inf')) 
    return float('inf') # Out of bounds

def astar_search_generator(maze, start, goal):
    """
    Performs A* search on the maze and yields the state at each step.
    Goal is fixed at the provided 'goal' coordinate.
    Handles special treasure cost only if the goal itself is treasure.
    """
    rows, cols = len(maze), len(maze[0])
    open_list_heap = []
    open_list_positions = set()
    closed_list_positions = set()
    nodes_map = {}

    start_node = Node(start, g=0, h=heuristic(start, goal))
    heapq.heappush(open_list_heap, start_node)
    open_list_positions.add(start)
    nodes_map[start] = start_node

    yield {'current': None, 'open': open_list_positions.copy(), 'closed': closed_list_positions.copy(), 'path': None}

    while open_list_heap:
        current_node = heapq.heappop(open_list_heap)
        open_list_positions.remove(current_node.position)

        yield {'current': current_node.position, 'open': open_list_positions.copy(), 'closed': closed_list_positions.copy(), 'path': None}

        if current_node.position == goal:
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp.position)
                temp = temp.parent
            yield {'current': current_node.position, 'open': open_list_positions.copy(), 'closed': closed_list_positions.copy(), 'path': path[::-1]}
            return

        closed_list_positions.add(current_node.position)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (current_node.position[0] + dr, current_node.position[1] + dc)
            r, c = neighbor_pos

            if not (0 <= r < rows and 0 <= c < cols): continue
            if maze[r][c] == 0: continue # Wall
            if neighbor_pos in closed_list_positions: continue

            # Calculate cost
            movement_cost = get_cost(maze, neighbor_pos)
            g_cost = current_node.g + movement_cost

            # Apply special treasure cost *only* if this neighbor *is* the goal *and* goal is treasure
            if neighbor_pos == goal and maze[r][c] == 4:
                 # Cost to *reach* goal is current_g + treasure_cost
                 g_cost = current_node.g + COSTS[4] 
                 # Recalculate movement cost for this step using treasure cost
                 movement_cost = COSTS[4]
            elif maze[r][c] == 4:
                 # If neighbor is treasure but *not* the goal, treat as impassable or assign high cost?
                 # For now, let's just use its base cost (which is -1, potentially problematic). 
                 # Let's treat non-goal treasure as normal road for movement cost calculation.
                 movement_cost = COSTS[1] 
                 g_cost = current_node.g + movement_cost

            h_cost = heuristic(neighbor_pos, goal)
            neighbor_node = Node(neighbor_pos, parent=current_node, g=g_cost, h=h_cost)

            if neighbor_pos in open_list_positions:
                existing_node = nodes_map[neighbor_pos]
                if existing_node.f <= neighbor_node.f: continue
            
            heapq.heappush(open_list_heap, neighbor_node)
            open_list_positions.add(neighbor_pos)
            nodes_map[neighbor_pos] = neighbor_node

    yield {'current': None, 'open': open_list_positions.copy(), 'closed': closed_list_positions.copy(), 'path': None}


# --- Example Usage --- 
if __name__ == "__main__":
    maze = [
        [1, 1, 0, 1, 1, 1, 1, 1],
        [1, 2, 1, 1, 3, 0, 1, 1],
        [1, 2, 0, 0, 1, 1, 3, 1],
        [1, 1, 1, 3, 1, 0, 2, 1],
        [0, 3, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 4, 1], # Treasure is no longer necessarily the goal
        [1, 3, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 2, 1, 1, 1, 1]  # Goal is here (bottom-right)
    ]
    rows, cols = len(maze), len(maze[0])
    start_pos = (0, 0)
    goal_pos = (rows - 1, cols - 1) # Explicitly set goal to bottom-right

    print(f"Start: {start_pos}, Goal: {goal_pos}")
        
    search_generator = astar_search_generator(maze, start_pos, goal_pos)
        
    # --- Animation Setup ---
    fig, ax = plt.subplots(figsize=(10, 10 * len(maze) / len(maze[0]))) # Corrected figsize based on actual rows/cols
        
    search_frames = list(search_generator)
    final_state = search_frames[-1]
    final_path = final_state.get('path')

    # --- Animation Update Function ---
    def update_plot(frame_data, ax, maze, start_pos, goal_pos, final_path):
        ax.clear() 
        current = frame_data['current']
        open_set = frame_data['open']
        closed_set = frame_data['closed']
            
        visualize_maze_step(ax, maze, current, open_set, closed_set, start_pos, goal_pos)
            
        step_num = search_frames.index(frame_data)
        title = f"A* Search Step: {step_num}"
            
        if frame_data == final_state:
            if final_path:
                title = f"A* Search Complete - Path Found (Step {step_num})"
                y, x = zip(*final_path)
                ax.plot(x, y, color='#FF00FF', linestyle='-', linewidth=3, alpha=0.8, label='Final Path')
                handles, labels = ax.get_legend_handles_labels()
                # Avoid adding duplicate 'Final Path' label if already present
                if not any(label == 'Final Path' for label in labels):
                     handles.append(mpatches.Patch(color='#FF00FF', label='Final Path'))
                ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize='x-small')
            else:
                title = f"A* Search Complete - No Path Found (Step {step_num})"

        ax.set_title(title)

    # --- Create and Show Animation ---
    ani = animation.FuncAnimation(fig, update_plot, frames=search_frames, 
                                  fargs=(ax, maze, start_pos, goal_pos, final_path), 
                                  interval=600, 
                                  repeat=False)

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

    if final_path:
        print("Path found.") 
    else:
        print("No path found.")

