"""
Analytics module for tracking pathfinding performance.
Uses Binary Search Tree for efficient sorted storage.
"""

import statistics


class BSTNode:
    """Node in Binary Search Tree for storing performance data"""
    
    def __init__(self, duration, algorithm_name="Unknown"):
        self.duration = duration
        self.algorithm_name = algorithm_name
        self.count = 1
        self.left = None
        self.right = None
        self.runs = []  # Store individual run details


class Analytics:
    """Analytics tracker for maze solving performance"""
    
    def __init__(self):
        self.path_history_tree = None
        self.solved_mazes = {}
        self.all_runs = []
        self.algorithm_stats = {}
    
    def generate_key(self, width, height, depth, start, goal):
        """Generate unique key for a maze configuration"""
        return f"{width}x{height}x{depth}|{start.x},{start.y},{start.z}|{goal.x},{goal.y},{goal.z}"
    
    def insert_into_bst(self, duration, algorithm_name="Unknown", metadata=None):
        """
        Insert a run duration into the BST.
        
        Args:
            duration: Time taken in milliseconds
            algorithm_name: Name of the algorithm used
            metadata: Additional run information (dict)
        """
        if self.path_history_tree is None:
            self.path_history_tree = BSTNode(duration, algorithm_name)
            if metadata:
                self.path_history_tree.runs.append(metadata)
        else:
            self._insert_recursive(self.path_history_tree, duration, algorithm_name, metadata)
        
        # Track algorithm statistics
        if algorithm_name not in self.algorithm_stats:
            self.algorithm_stats[algorithm_name] = {
                'runs': 0,
                'total_time': 0,
                'total_nodes_explored': 0,
                'total_path_length': 0,
                'best_time': float('inf'),
                'worst_time': 0
            }
        
        stats = self.algorithm_stats[algorithm_name]
        stats['runs'] += 1
        stats['total_time'] += duration
        stats['best_time'] = min(stats['best_time'], duration)
        stats['worst_time'] = max(stats['worst_time'], duration)
        
        if metadata:
            if 'nodes_explored' in metadata:
                stats['total_nodes_explored'] += metadata['nodes_explored']
            if 'path_length' in metadata:
                stats['total_path_length'] += metadata['path_length']
        
        # Store in all runs list
        self.all_runs.append({
            'duration': duration,
            'algorithm': algorithm_name,
            'metadata': metadata
        })
    
    def _insert_recursive(self, current_node, duration, algorithm_name, metadata):
        """Recursively insert into BST"""
        if duration < current_node.duration:
            if current_node.left is None:
                current_node.left = BSTNode(duration, algorithm_name)
                if metadata:
                    current_node.left.runs.append(metadata)
            else:
                self._insert_recursive(current_node.left, duration, algorithm_name, metadata)
        elif duration > current_node.duration:
            if current_node.right is None:
                current_node.right = BSTNode(duration, algorithm_name)
                if metadata:
                    current_node.right.runs.append(metadata)
            else:
                self._insert_recursive(current_node.right, duration, algorithm_name, metadata)
        else:
            # Same duration, increment count
            current_node.count += 1
            if metadata:
                current_node.runs.append(metadata)
    
    def display_stats_inorder(self, node=None):
        """Display all run statistics in sorted order"""
        if node is None:
            node = self.path_history_tree
        
        if node:
            self.display_stats_inorder(node.left)
            print(f"Duration: {node.duration:.2f} ms | "
                  f"Algorithm: {node.algorithm_name} | "
                  f"Frequency: {node.count}")
            self.display_stats_inorder(node.right)
    
    def find_fastest_run(self):
        """Find the fastest run (leftmost node in BST)"""
        if self.path_history_tree is None:
            return None
        
        current = self.path_history_tree
        while current.left is not None:
            current = current.left
        
        return {
            'duration': current.duration,
            'algorithm': current.algorithm_name,
            'count': current.count
        }
    
    def find_slowest_run(self):
        """Find the slowest run (rightmost node in BST)"""
        if self.path_history_tree is None:
            return None
        
        current = self.path_history_tree
        while current.right is not None:
            current = current.right
        
        return {
            'duration': current.duration,
            'algorithm': current.algorithm_name,
            'count': current.count
        }
    
    def print_leaderboard(self, node=None, first_call=True, limit=10):
        """Print top N fastest runs"""
        if first_call:
            node = self.path_history_tree
            print("\n" + "="*70)
            print("PERFORMANCE LEADERBOARD (Fastest to Slowest)")
            print("="*70)
            self._count = 0
            self._limit = limit
        
        if node is not None and self._count < self._limit:
            # Traverse left (faster times)
            self.print_leaderboard(node.left, False, limit)
            
            # Print current if within limit
            if self._count < self._limit:
                self._count += 1
                print(f"#{self._count:2d} | {node.duration:8.2f} ms | "
                      f"{node.algorithm_name:20s} | Count: {node.count}")
            
            # Traverse right (slower times)
            self.print_leaderboard(node.right, False, limit)
        
        if first_call:
            print("="*70)
    
    def get_algorithm_summary(self):
        """Get summary statistics for each algorithm"""
        summary = {}
        
        for algo_name, stats in self.algorithm_stats.items():
            if stats['runs'] > 0:
                summary[algo_name] = {
                    'runs': stats['runs'],
                    'avg_time': stats['total_time'] / stats['runs'],
                    'best_time': stats['best_time'],
                    'worst_time': stats['worst_time'],
                    'avg_nodes_explored': stats['total_nodes_explored'] / stats['runs'] 
                                         if stats['total_nodes_explored'] > 0 else 0,
                    'avg_path_length': stats['total_path_length'] / stats['runs']
                                      if stats['total_path_length'] > 0 else 0
                }
        
        return summary
    
    def print_algorithm_comparison(self):
        """Print detailed comparison of all algorithms"""
        summary = self.get_algorithm_summary()
        
        if not summary:
            print("No data to compare yet.")
            return
        
        print("\n" + "="*90)
        print("ALGORITHM COMPARISON")
        print("="*90)
        print(f"{'Algorithm':<20} | {'Runs':>6} | {'Avg Time':>10} | "
              f"{'Best':>10} | {'Worst':>10} | {'Avg Nodes':>10}")
        print("-"*90)
        
        for algo_name, stats in sorted(summary.items(), 
                                       key=lambda x: x[1]['avg_time']):
            print(f"{algo_name:<20} | {stats['runs']:>6} | "
                  f"{stats['avg_time']:>9.2f}ms | "
                  f"{stats['best_time']:>9.2f}ms | "
                  f"{stats['worst_time']:>9.2f}ms | "
                  f"{stats['avg_nodes_explored']:>10.1f}")
        
        print("="*90)
    
    def get_statistics(self):
        """Get overall statistics across all runs"""
        if not self.all_runs:
            return None
        
        durations = [run['duration'] for run in self.all_runs]
        
        return {
            'total_runs': len(self.all_runs),
            'mean_duration': statistics.mean(durations),
            'median_duration': statistics.median(durations),
            'stdev_duration': statistics.stdev(durations) if len(durations) > 1 else 0,
            'min_duration': min(durations),
            'max_duration': max(durations),
            'algorithms_used': len(self.algorithm_stats)
        }
    
    def export_data(self):
        """Export all data for external analysis"""
        return {
            'all_runs': self.all_runs,
            'algorithm_stats': self.algorithm_stats,
            'statistics': self.get_statistics()
        }
    
    def clear_data(self):
        """Clear all analytics data"""
        self.path_history_tree = None
        self.solved_mazes = {}
        self.all_runs = []
        self.algorithm_stats = {}
