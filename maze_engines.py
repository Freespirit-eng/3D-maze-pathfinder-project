"""
3D Maze Engine with Recursive Backtracking (DFS) algorithm.
Generates perfect mazes (no loops, exactly one path between any two points).
"""

import random
from node import Node


class MazeEngine:
    def __init__(self, width, height, depth):
        """
        Initialize 3D maze grid.
        
        Args:
            width: Size in X dimension
            height: Size in Y dimension  
            depth: Size in Z dimension
        """
        self.width = width
        self.height = height
        self.depth = depth
        
        # Create 3D grid of nodes (all start as unvisited paths)
        self.grid = [[[Node(x, y, z, is_wall=False) 
                      for z in range(depth)] 
                      for y in range(height)] 
                      for x in range(width)]
        
        self.generation_algorithm = "Recursive Backtracking (DFS)"
    
    def get_node(self, x, y, z):
        """Safely get a node from the grid"""
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            return self.grid[x][y][z]
        return None
    
    def get_unvisited_neighbors(self, node):
        """Get all unvisited neighboring cells for maze generation"""
        neighbors = []
        directions = [
            (1, 0, 0, 'east'),   # +X
            (-1, 0, 0, 'west'),  # -X
            (0, 1, 0, 'up'),     # +Y
            (0, -1, 0, 'down'),  # -Y
            (0, 0, 1, 'north'),  # +Z
            (0, 0, -1, 'south')  # -Z
        ]
        
        for dx, dy, dz, direction in directions:
            nx, ny, nz = node.x + dx, node.y + dy, node.z + dz
            if 0 <= nx < self.width and 0 <= ny < self.height and 0 <= nz < self.depth:
                neighbor = self.grid[nx][ny][nz]
                if not neighbor.visited:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def get_neighbors(self, node):
        """Get all accessible neighboring cells (no walls between them)"""
        neighbors = []
        directions = [
            (1, 0, 0),   # +X (east)
            (-1, 0, 0),  # -X (west)
            (0, 1, 0),   # +Y (up)
            (0, -1, 0),  # -Y (down)
            (0, 0, 1),   # +Z (north)
            (0, 0, -1)   # -Z (south)
        ]
        
        for dx, dy, dz in directions:
            nx, ny, nz = node.x + dx, node.y + dy, node.z + dz
            if 0 <= nx < self.width and 0 <= ny < self.height and 0 <= nz < self.depth:
                neighbor = self.grid[nx][ny][nz]
                # Check if wall exists between current node and neighbor
                if not node.has_wall_to(neighbor) and not neighbor.is_wall:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def recursive_backtracking(self, current):
        """
        Recursive Backtracking (DFS) maze generation algorithm.
        Creates a perfect maze with no loops.
        
        Args:
            current: Current node being processed
        """
        current.visited = True
        
        # Get all unvisited neighbors
        neighbors = self.get_unvisited_neighbors(current)
        
        # Shuffle for randomness
        random.shuffle(neighbors)
        
        # Visit each unvisited neighbor
        for neighbor in neighbors:
            if not neighbor.visited:
                # Remove wall between current and neighbor
                current.remove_wall_to(neighbor)
                
                # Recursively visit the neighbor
                self.recursive_backtracking(neighbor)
    
    def generate_maze(self, algorithm="recursive_backtracking", start_pos=None):
        """
        Generate a 3D maze using specified algorithm.
        
        Args:
            algorithm: Algorithm to use ("recursive_backtracking" or "kruskal")
            start_pos: Starting position tuple (x, y, z), defaults to (0, 0, 0)
        """
        # Reset all nodes
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    self.grid[x][y][z].reset_maze_generation()
        
        if algorithm == "recursive_backtracking":
            # Start from specified position or (0, 0, 0)
            if start_pos is None:
                start_pos = (0, 0, 0)
            
            start_node = self.grid[start_pos[0]][start_pos[1]][start_pos[2]]
            self.recursive_backtracking(start_node)
            self.generation_algorithm = "Recursive Backtracking (DFS)"
            
        elif algorithm == "kruskal":
            self._generate_kruskal()
            self.generation_algorithm = "Kruskal's Algorithm (MST)"
        
        # Ensure all nodes are marked as non-walls (paths)
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    self.grid[x][y][z].is_wall = False
    
    def _generate_kruskal(self):
        """
        Alternative: Kruskal's algorithm for maze generation.
        Uses Union-Find to create a minimum spanning tree.
        """
        from maze_utils import UnionFind
        
        uf = UnionFind(self.width * self.height * self.depth)
        
        # Create list of all possible edges
        edges = []
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    node = self.grid[x][y][z]
                    
                    # Add edge to east neighbor
                    if x + 1 < self.width:
                        neighbor = self.grid[x + 1][y][z]
                        edges.append((node, neighbor))
                    
                    # Add edge to up neighbor
                    if y + 1 < self.height:
                        neighbor = self.grid[x][y + 1][z]
                        edges.append((node, neighbor))
                    
                    # Add edge to north neighbor
                    if z + 1 < self.depth:
                        neighbor = self.grid[x][y][z + 1]
                        edges.append((node, neighbor))
        
        # Shuffle edges for randomness
        random.shuffle(edges)
        
        # Process edges
        for node1, node2 in edges:
            id1 = self._get_id(node1.x, node1.y, node1.z)
            id2 = self._get_id(node2.x, node2.y, node2.z)
            
            # If nodes are in different sets, connect them
            if uf.union(id1, id2):
                node1.remove_wall_to(node2)
                node1.visited = True
                node2.visited = True
    
    def _get_id(self, x, y, z):
        """Convert 3D coordinates to unique ID"""
        return z * (self.width * self.height) + y * self.width + x
    
    def reset_pathfinding(self):
        """Reset all pathfinding-related node attributes"""
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    self.grid[x][y][z].reset_pathfinding()
    
    def get_maze_stats(self):
        """Get statistics about the generated maze"""
        total_cells = self.width * self.height * self.depth
        total_walls = 0
        total_openings = 0
        
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    node = self.grid[x][y][z]
                    for wall in node.walls.values():
                        if wall:
                            total_walls += 1
                        else:
                            total_openings += 1
        
        # Each wall is counted twice (once from each side)
        total_walls //= 2
        total_openings //= 2
        
        return {
            'total_cells': total_cells,
            'total_walls': total_walls,
            'total_openings': total_openings,
            'dimensions': f"{self.width}×{self.height}×{self.depth}",
            'algorithm': self.generation_algorithm
        }
