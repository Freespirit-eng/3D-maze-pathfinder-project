"""
Node class for 3D maze representation.
Each node represents a cell in the 3D grid with thick walls for voxel visualization.
"""

class Node:
    def __init__(self, x, y, z, is_wall=False):
        # Spatial coordinates
        self.x = x
        self.y = y
        self.z = z
        
        # Wall state
        self.is_wall = is_wall
        
        # Wall connectivity for thick-wall visualization
        # These represent which walls are present around this cell
        self.walls = {
            'north': True,   # +Z direction
            'south': True,   # -Z direction
            'east': True,    # +X direction
            'west': True,    # -X direction
            'up': True,      # +Y direction
            'down': True     # -Y direction
        }
        
        # Pathfinding scores (A* algorithm)
        self.g_score = float('inf')  # Cost from start to here
        self.h_score = 0              # Heuristic cost to goal
        self.f_score = float('inf')  # Total cost (g + h)
        
        # Dijkstra's algorithm score
        self.distance = float('inf')
        
        # Path reconstruction
        self.parent = None
        
        # Maze generation tracking
        self.visited = False
        
    def __lt__(self, other):
        """Comparison for priority queue (based on f_score for A*)"""
        return self.f_score < other.f_score
    
    def __eq__(self, other):
        """Equality based on coordinates"""
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        """Hash based on coordinates for use in sets/dicts"""
        return hash((self.x, self.y, self.z))
    
    def reset_pathfinding(self):
        """Reset pathfinding-related attributes"""
        self.g_score = float('inf')
        self.h_score = 0
        self.f_score = float('inf')
        self.distance = float('inf')
        self.parent = None
    
    def reset_maze_generation(self):
        """Reset maze generation attributes"""
        self.visited = False
        self.walls = {
            'north': True,
            'south': True,
            'east': True,
            'west': True,
            'up': True,
            'down': True
        }
    
    def remove_wall_to(self, neighbor):
        """Remove wall between this node and a neighbor"""
        dx = neighbor.x - self.x
        dy = neighbor.y - self.y
        dz = neighbor.z - self.z
        
        # Remove appropriate walls
        if dx == 1:  # Neighbor is to the east
            self.walls['east'] = False
            neighbor.walls['west'] = False
        elif dx == -1:  # Neighbor is to the west
            self.walls['west'] = False
            neighbor.walls['east'] = False
        elif dy == 1:  # Neighbor is up
            self.walls['up'] = False
            neighbor.walls['down'] = False
        elif dy == -1:  # Neighbor is down
            self.walls['down'] = False
            neighbor.walls['up'] = False
        elif dz == 1:  # Neighbor is to the north
            self.walls['north'] = False
            neighbor.walls['south'] = False
        elif dz == -1:  # Neighbor is to the south
            self.walls['south'] = False
            neighbor.walls['north'] = False
    
    def has_wall_to(self, neighbor):
        """Check if there's a wall between this node and a neighbor"""
        dx = neighbor.x - self.x
        dy = neighbor.y - self.y
        dz = neighbor.z - self.z
        
        if dx == 1:
            return self.walls['east']
        elif dx == -1:
            return self.walls['west']
        elif dy == 1:
            return self.walls['up']
        elif dy == -1:
            return self.walls['down']
        elif dz == 1:
            return self.walls['north']
        elif dz == -1:
            return self.walls['south']
        
        return True  # Not a neighbor
    
    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.z}, wall={self.is_wall})"
