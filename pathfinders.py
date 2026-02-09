"""
Pathfinding algorithms for 3D maze solving.
Includes A*, BFS, and Dijkstra's algorithm.
"""

import heapq
from collections import deque
from maze_utils import manhattan_distance_3d, euclidean_distance_3d


def reconstruct_path(current_node):
    """
    Reconstruct path from goal to start using parent pointers.
    Returns list of coordinate tuples from start to goal.
    """
    path = []
    temp = current_node
    
    while temp is not None:
        path.append((temp.x, temp.y, temp.z))
        temp = temp.parent
    
    return path[::-1]  # Reverse to get start -> goal


def a_star(start_node, goal_node, maze, heuristic="manhattan"):
    """
    A* pathfinding algorithm with configurable heuristic.
    
    Args:
        start_node: Starting node
        goal_node: Goal node
        maze: MazeEngine instance
        heuristic: Heuristic function name ("manhattan" or "euclidean")
    
    Returns:
        tuple: (path, nodes_explored, visited_count, visited_order)
    """
    # Reset pathfinding state
    maze.reset_pathfinding()
    
    # Choose heuristic function
    if heuristic == "euclidean":
        heuristic_func = euclidean_distance_3d
    else:
        heuristic_func = manhattan_distance_3d
    
    # Initialize start node
    start_node.g_score = 0
    start_node.h_score = heuristic_func(start_node, goal_node)
    start_node.f_score = start_node.h_score
    
    # Priority queue and tracking
    open_set = []
    heapq.heappush(open_set, (start_node.f_score, id(start_node), start_node))
    open_set_nodes = {start_node}
    
    visited_count = 0
    visited_order = []
    
    while open_set:
        # Get node with lowest f_score
        _, _, current = heapq.heappop(open_set)
        
        if current in open_set_nodes:
            open_set_nodes.remove(current)
        
        visited_count += 1
        visited_order.append((current.x, current.y, current.z))
        
        # Check if goal reached
        if current == goal_node:
            path = reconstruct_path(current)
            return path, visited_count, len(visited_order), visited_order
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current):
            tentative_g_score = current.g_score + 1
            
            if tentative_g_score < neighbor.g_score:
                # This path to neighbor is better
                neighbor.parent = current
                neighbor.g_score = tentative_g_score
                neighbor.h_score = heuristic_func(neighbor, goal_node)
                neighbor.f_score = neighbor.g_score + neighbor.h_score
                
                if neighbor not in open_set_nodes:
                    heapq.heappush(open_set, (neighbor.f_score, id(neighbor), neighbor))
                    open_set_nodes.add(neighbor)
    
    # No path found
    return None, visited_count, len(visited_order), visited_order


def bfs(start_node, goal_node, maze):
    """
    Breadth-First Search pathfinding algorithm.
    Guarantees shortest path but explores many nodes.
    
    Args:
        start_node: Starting node
        goal_node: Goal node
        maze: MazeEngine instance
    
    Returns:
        tuple: (path, nodes_explored, visited_count, visited_order)
    """
    # Reset pathfinding state
    maze.reset_pathfinding()
    
    queue = deque([start_node])
    visited = {start_node}
    visited_count = 0
    visited_order = []
    
    while queue:
        current = queue.popleft()
        visited_count += 1
        visited_order.append((current.x, current.y, current.z))
        
        # Check if goal reached
        if current == goal_node:
            path = reconstruct_path(current)
            return path, visited_count, len(visited_order), visited_order
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                queue.append(neighbor)
    
    # No path found
    return None, visited_count, len(visited_order), visited_order


def dijkstra(start_node, goal_node, maze):
    """
    Dijkstra's algorithm for pathfinding.
    Similar to A* but without heuristic (uniform cost search).
    
    Args:
        start_node: Starting node
        goal_node: Goal node
        maze: MazeEngine instance
    
    Returns:
        tuple: (path, nodes_explored, visited_count, visited_order)
    """
    # Reset pathfinding state
    maze.reset_pathfinding()
    
    # Initialize start node
    start_node.distance = 0
    
    # Priority queue: (distance, unique_id, node)
    pq = []
    heapq.heappush(pq, (0, id(start_node), start_node))
    
    visited = set()
    visited_count = 0
    visited_order = []
    
    while pq:
        current_distance, _, current = heapq.heappop(pq)
        
        # Skip if already visited
        if current in visited:
            continue
        
        visited.add(current)
        visited_count += 1
        visited_order.append((current.x, current.y, current.z))
        
        # Check if goal reached
        if current == goal_node:
            path = reconstruct_path(current)
            return path, visited_count, len(visited_order), visited_order
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited:
                new_distance = current_distance + 1
                
                if new_distance < neighbor.distance:
                    neighbor.distance = new_distance
                    neighbor.parent = current
                    heapq.heappush(pq, (new_distance, id(neighbor), neighbor))
    
    # No path found
    return None, visited_count, len(visited_order), visited_order


# Algorithm registry for easy access
ALGORITHMS = {
    'a_star': a_star,
    'bfs': bfs,
    'dijkstra': dijkstra
}


def get_algorithm(name):
    """Get pathfinding algorithm by name"""
    return ALGORITHMS.get(name.lower())

