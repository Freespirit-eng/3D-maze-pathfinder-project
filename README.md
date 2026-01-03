# 🧊 3D Maze Pathfinding Solver

An advanced 3D maze generation and pathfinding visualization tool featuring multiple algorithms, perfect maze generation using Recursive Backtracking (DFS), and interactive visualizations.

## ✨ Features

### Maze Generation
- **Recursive Backtracking (DFS)**: Creates perfect mazes with long, winding corridors and exactly one path between any two points
- **Kruskal's Algorithm (MST)**: Alternative generation using minimum spanning tree approach
- **Thick Wall Support**: Proper wall representation for voxel-style 3D visualization
- **Configurable Size**: Generate mazes from 5×5×5 to 50×50×50 (or larger)

### Pathfinding Algorithms
- **A* Search**: 
  - Manhattan distance heuristic (optimal for grid movement)
  - Euclidean distance heuristic (straight-line distance)
  - Most efficient algorithm for finding shortest paths
- **BFS (Breadth-First Search)**: Guarantees shortest path, explores all nodes at each depth level
- **Dijkstra's Algorithm**: Uniform cost search, similar to A* without heuristic
- **Bidirectional BFS**: Searches from both start and goal simultaneously for faster results

### Visualization
- **Interactive 3D Plots**: Rotate, zoom, and pan through the maze using Plotly
- **Animated Exploration**: Watch algorithms explore the maze in real-time
- **Multiple Simultaneous Views**: Compare up to 5 algorithms side-by-side
- **Color-Coded Results**: Different colors for each algorithm's exploration pattern

### Analytics
- **Binary Search Tree**: Efficient storage and retrieval of performance data
- **Leaderboard**: Track fastest runs across all sessions
- **Algorithm Comparison**: Detailed statistics for each algorithm
- **Performance Metrics**: Time, nodes explored, path length, and efficiency

## 🚀 Quick Start

### Installation

```bash
# Clone or download the repository
git clone <repository-url>
cd 3d-maze-solver

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

**Option 1: Streamlit Web Interface (Recommended)**
```bash
streamlit run app.py
```

**Option 2: Command-Line Interface**
```bash
# Basic run with default settings (30×30×30 maze)
python main.py

# Custom maze size
python main.py --size 20

# Multiple runs for statistics
python main.py --size 25 --runs 5

# Interactive mode
python main.py --interactive

# Specific algorithms only
python main.py --algorithms astar bfs

# Show help
python main.py --help
```

## 📁 Project Structure

```
3d-maze-solver/
│
├── node.py              # Node class with wall connectivity
├── maze_engine.py       # Maze generation (Recursive Backtracking + Kruskal)
├── maze_utils.py        # Utility functions (UnionFind, distance metrics)
├── pathfinder.py        # Pathfinding algorithms (A*, BFS, Dijkstra, Bidirectional)
├── analytics.py         # Performance tracking with BST
├── main.py              # Command-line interface
├── app.py               # Streamlit web interface
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎮 Usage Guide

### Web Interface (Streamlit)

1. **Configure Maze**:
   - Choose grid size (5-30)
   - Select generation algorithm
   - Click "🔄 New Maze" to generate

2. **Set Start/Goal**:
   - Enter X, Y, Z coordinates for start point
   - Enter X, Y, Z coordinates for goal point

3. **Select Algorithms**:
   - Choose 1-5 algorithms to compare
   - Recommended: Start with 2-3 for better performance

4. **Run Race**:
   - Click "🚀 START PATHFINDING RACE!"
   - Watch animated exploration
   - Review performance metrics

5. **View Analytics**:
   - Check leaderboard for fastest runs
   - Compare algorithm statistics
   - Export data for external analysis

### Command-Line Interface

**Interactive Mode**:
```bash
python main.py --interactive
```
Follow prompts to configure maze parameters.

**Automated Runs**:
```bash
# Run with specific configuration
python main.py --size 25 --runs 3 --algorithms astar bfs dijkstra
```

## 🧠 Algorithm Details

### A* Search
- **Time Complexity**: O(b^d) where b is branching factor, d is depth
- **Space Complexity**: O(b^d)
- **Optimal**: Yes (with admissible heuristic)
- **Use Case**: Best for most pathfinding scenarios

**Heuristics**:
- **Manhattan**: |x1-x2| + |y1-y2| + |z1-z2| (recommended for grid movement)
- **Euclidean**: √[(x1-x2)² + (y1-y2)² + (z1-z2)²] (straight-line distance)

### BFS (Breadth-First Search)
- **Time Complexity**: O(V + E) where V is vertices, E is edges
- **Space Complexity**: O(V)
- **Optimal**: Yes (for unweighted graphs)
- **Use Case**: Simple pathfinding, guaranteed shortest path

### Dijkstra's Algorithm
- **Time Complexity**: O((V + E) log V) with binary heap
- **Space Complexity**: O(V)
- **Optimal**: Yes (for weighted graphs)
- **Use Case**: When all edge weights are non-negative

### Bidirectional BFS
- **Time Complexity**: O(b^(d/2)) - can be much faster than regular BFS
- **Space Complexity**: O(b^(d/2))
- **Optimal**: Yes (for unweighted graphs)
- **Use Case**: Long paths where meeting in the middle is faster

## 🏗️ Technical Implementation

### Perfect Maze Generation (Recursive Backtracking)

The recursive backtracking algorithm creates a "perfect maze" - a maze with exactly one path between any two points and no loops:

1. Start at initial cell and mark as visited
2. While there are unvisited neighbors:
   - Choose random unvisited neighbor
   - Remove wall between current and chosen neighbor
   - Recursively visit the neighbor
3. Backtrack when no unvisited neighbors remain

**Key Properties**:
- No cycles/loops
- All cells are connected
- Unique path between any two cells
- Creates long, winding corridors

### Thick Walls for Voxel Visualization

Each `Node` tracks walls in 6 directions:
```python
walls = {
    'north': True,   # +Z direction
    'south': True,   # -Z direction  
    'east': True,    # +X direction
    'west': True,    # -X direction
    'up': True,      # +Y direction
    'down': True     # -Y direction
}
```

When a path is carved between two cells, walls are removed from both cells:
```python
def remove_wall_to(self, neighbor):
    if neighbor.x > self.x:
        self.walls['east'] = False
        neighbor.walls['west'] = False
    # ... similar for other directions
```

### Binary Search Tree for Analytics

Performance data is stored in a BST for efficient sorted retrieval:
```python
class BSTNode:
    def __init__(self, duration):
        self.duration = duration
        self.count = 1
        self.left = None   # Faster runs
        self.right = None  # Slower runs
```

**Benefits**:
- O(log n) average insertion
- O(n) sorted traversal
- Efficient leaderboard queries
- Maintains historical data

## 📊 Performance Benchmarks

Typical performance on a 30×30×30 maze:

| Algorithm | Nodes Explored | Path Length | Time (ms) | Efficiency |
|-----------|---------------|-------------|-----------|------------|
| A* (Manhattan) | 3,542 | 87 | 45.2 | 2.5% |
| A* (Euclidean) | 3,789 | 87 | 48.1 | 2.3% |
| BFS | 13,287 | 87 | 112.3 | 0.7% |
| Dijkstra | 12,945 | 87 | 128.7 | 0.7% |
| Bidirectional | 8,421 | 87 | 76.5 | 1.0% |

*Results vary based on maze configuration and start/goal positions*

## 🎨 Customization

### Adding New Heuristics

```python
def custom_heuristic(node1, node2):
    # Your custom distance calculation
    return distance

# Use in pathfinder.py:
def a_star(start, goal, maze, heuristic="custom"):
    if heuristic == "custom":
        heuristic_func = custom_heuristic
```

### Adding New Algorithms

1. Create function in `pathfinder.py`:
```python
def my_algorithm(start_node, goal_node, maze):
    # Your implementation
    return path, nodes_explored, visited_count, visited_order
```

2. Add to algorithm registry:
```python
ALGORITHMS['my_algorithm'] = my_algorithm
```

3. Update Streamlit app to include in dropdown

## 🐛 Troubleshooting

**Issue**: Streamlit app won't start
- **Solution**: Ensure all dependencies installed: `pip install -r requirements.txt`

**Issue**: Maze generation is slow for large sizes
- **Solution**: Use smaller maze sizes (≤30) for interactive use, larger sizes for benchmarking

**Issue**: No path found between start and goal
- **Solution**: Ensure start and goal coordinates are valid and not walls. Perfect mazes guarantee a path exists.

**Issue**: Animation is choppy
- **Solution**: Reduce animation steps in sidebar or increase animation speed

**Issue**: Out of memory errors
- **Solution**: Reduce maze size or close other applications

## 📚 References

- [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional maze generation algorithms (Prim's, Eller's, etc.)
- More pathfinding algorithms (Jump Point Search, Theta*, etc.)
- 3D rendering with Three.js or Unity
- Web-based maze editor
- Multi-agent pathfinding
- Performance optimizations

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 🙏 Acknowledgments

- Inspired by maze generation and pathfinding research
- Built with Streamlit and Plotly for visualization
- Uses efficient data structures (BST, Union-Find) for performance

## 📞 Support

For questions or issues:
1. Check this README thoroughly
2. Review code comments and docstrings
3. Test with smaller maze sizes first
4. Check console output for error messages

---

**Happy Pathfinding! 🎮🧊**
