# 🚀 Quick Start Guide

## Installation (30 seconds)

```bash
# Install dependencies
pip install streamlit plotly numpy

# Or use requirements file
pip install -r requirements.txt
```

## Run the Project (Choose One)

### Option 1: Web Interface (Recommended) 🌐
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

### Option 2: Command Line 💻
```bash
# Basic run (30×30×30 maze)
python main.py

# Custom size
python main.py --size 20

# Interactive mode
python main.py --interactive
```

### Option 3: Test Everything ✅
```bash
python test_maze.py
```

## First Steps in Web Interface

1. **Generate a Maze**
   - Click "🔄 New Maze" in sidebar
   - Choose size (start with 10-15)

2. **Set Points**
   - Start: Usually (0, 0, 0)
   - Goal: Usually (size-1, size-1, size-1)

3. **Select Algorithms**
   - Try: "A* (Manhattan)" and "BFS"
   - Start with 2-3 algorithms

4. **Run Race**
   - Click "🚀 START PATHFINDING RACE!"
   - Watch the visualization
   - Review performance metrics

## Tips for Best Results

✅ **Start small**: Use 10×10×10 for first runs
✅ **Compare 2-3 algorithms**: More algorithms = slower visualization
✅ **Adjust animation speed**: Lower = faster (try 0.01)
✅ **Try different start/goal positions**: See how algorithms adapt

## Common Commands

```bash
# Quick 20×20×20 maze
python main.py --size 20

# Compare specific algorithms
python main.py --algorithms astar bfs

# Multiple runs for statistics
python main.py --size 15 --runs 5

# Interactive setup
python main.py -i

# Web interface
streamlit run app.py
```

## Troubleshooting

**Issue**: `ModuleNotFoundError`
→ **Fix**: `pip install streamlit plotly numpy`

**Issue**: Streamlit won't start
→ **Fix**: `pip install --upgrade streamlit`

**Issue**: Maze generation is slow
→ **Fix**: Use smaller maze size (≤20)

**Issue**: Animation is choppy
→ **Fix**: Reduce animation steps in sidebar

## What to Try

🎯 **Beginner**: 
- Run `streamlit run app.py`
- Generate 10×10×10 maze
- Compare A* vs BFS

🎯 **Intermediate**:
- Try different maze sizes
- Test all 4 algorithms
- Check analytics/leaderboard

🎯 **Advanced**:
- Run batch comparisons: `python main.py --size 30 --runs 10`
- Modify algorithms in `pathfinder.py`
- Add custom heuristics

## Project Structure

```
📁 3d-maze-solver/
├── 🐍 node.py              ← Node with thick walls
├── 🐍 maze_engine.py       ← Maze generation (DFS + Kruskal)
├── 🐍 pathfinder.py        ← All pathfinding algorithms
├── 🐍 analytics.py         ← Performance tracking
├── 🐍 main.py              ← CLI interface
├── 🐍 app.py               ← Web interface
├── 🐍 test_maze.py         ← Tests
├── 📄 README.md            ← Full documentation
└── 📄 IMPROVEMENTS.md      ← What's new
```

## Key Features

✨ **Maze Generation**
- Recursive Backtracking (DFS) - Perfect mazes
- Kruskal's Algorithm (MST) - Alternative style

✨ **Pathfinding**
- A* (Manhattan & Euclidean)
- BFS
- Dijkstra
- Bidirectional BFS

✨ **Visualization**
- 3D interactive plots
- Animated exploration
- Side-by-side comparison
- Performance metrics

✨ **Analytics**
- Leaderboard
- Algorithm comparison
- Performance tracking
- Export capabilities

## Next Steps

1. ✅ Run the test: `python test_maze.py`
2. ✅ Try the web interface: `streamlit run app.py`
3. ✅ Read the full README.md
4. ✅ Experiment with different algorithms
5. ✅ Check IMPROVEMENTS.md for what's new

---

**Need Help?**
- 📖 Read README.md for detailed documentation
- 🧪 Run test_maze.py to verify setup
- 💡 Check IMPROVEMENTS.md for feature details

**Ready to explore! 🎮**
