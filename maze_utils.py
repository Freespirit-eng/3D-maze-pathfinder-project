"""
Utility classes and functions for maze generation and algorithms.
"""


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure.
    Used for Kruskal's maze generation algorithm.
    """
    
    def __init__(self, n):
        """Initialize with n elements, each in its own set"""
        self.parent = list(range(n))
        self.rank = [0] * n
        self.num_sets = n
    
    def find(self, i):
        """Find the root of the set containing element i (with path compression)"""
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]
    
    def union(self, i, j):
        """
        Union the sets containing elements i and j.
        Returns True if union was performed, False if already in same set.
        """
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i == root_j:
            return False  # Already in same set
        
        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_i] = root_j
            self.rank[root_j] += 1
        
        self.num_sets -= 1
        return True
    
    def connected(self, i, j):
        """Check if elements i and j are in the same set"""
        return self.find(i) == self.find(j)


class Timer:
    """Simple timer for performance measurement"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer"""
        import time
        self.start_time = time.time()
    
    def stop(self):
        """Stop the timer and return elapsed time in milliseconds"""
        import time
        self.end_time = time.time()
        return (self.end_time - self.start_time) * 1000
    
    def elapsed_ms(self):
        """Get elapsed time in milliseconds"""
        if self.start_time is None:
            return 0
        import time
        current = self.end_time if self.end_time else time.time()
        return (current - self.start_time) * 1000


def manhattan_distance_3d(node1, node2):
    """Calculate 3D Manhattan distance between two nodes"""
    return abs(node1.x - node2.x) + abs(node1.y - node2.y) + abs(node1.z - node2.z)


def euclidean_distance_3d(node1, node2):
    """Calculate 3D Euclidean distance between two nodes"""
    dx = node1.x - node2.x
    dy = node1.y - node2.y
    dz = node1.z - node2.z
    return (dx*dx + dy*dy + dz*dz) ** 0.5


def chebyshev_distance_3d(node1, node2):
    """Calculate 3D Chebyshev distance (maximum coordinate difference)"""
    return max(abs(node1.x - node2.x), 
               abs(node1.y - node2.y), 
               abs(node1.z - node2.z))
