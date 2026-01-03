"""
Demo script to showcase voxel-style wall rendering.
Generates a small maze and displays it with thick voxel walls.
"""

from maze_engines import MazeEngine
from pathfinders import a_star
from voxel_visualizer import create_voxel_maze_visualization


def demo_voxel_visualization():
    """Create and visualize a small maze with voxel walls"""
    
    print("="*70)
    print(" "*20 + "🧊 VOXEL MAZE DEMO 🧊")
    print("="*70)
    
    # Create a small maze
    size = 8
    print(f"\n📦 Generating {size}×{size}×{size} maze...")
    engine = MazeEngine(size, size, size)
    engine.generate_maze(algorithm="recursive_backtracking")
    
    stats = engine.get_maze_stats()
    print(f"✅ Maze generated!")
    print(f"   - Total cells: {stats['total_cells']}")
    print(f"   - Total walls: {stats['total_walls']}")
    print(f"   - Total openings: {stats['total_openings']}")
    
    # Set start and goal
    start = engine.grid[0][0][0]
    goal = engine.grid[size-1][size-1][size-1]
    
    print(f"\n🎯 Finding path from (0,0,0) to ({size-1},{size-1},{size-1})...")
    
    # Run A* pathfinding
    import time
    start_time = time.time()
    path, count, v_len, order = a_star(start, goal, engine)
    duration = (time.time() - start_time) * 1000
    
    if path:
        print(f"✅ Path found!")
        print(f"   - Time: {duration:.2f}ms")
        print(f"   - Nodes explored: {v_len}")
        print(f"   - Path length: {len(path)}")
        print(f"   - Efficiency: {(len(path) / v_len * 100):.1f}%")
    else:
        print("❌ No path found!")
        return
    
    # Create visualization
    print(f"\n🎨 Creating voxel visualization...")
    print(f"   Note: Each wall is rendered as a 3D block with thickness")
    
    fig = create_voxel_maze_visualization(
        engine,
        visited_nodes=order,
        final_path=path,
        start=(0, 0, 0),
        goal=(size-1, size-1, size-1),
        title="Voxel Maze with Thick Walls",
        show_walls=True,
        wall_opacity=0.3,
        wall_color='gray'
    )
    
    print("✅ Visualization created!")
    print(f"\n💡 Opening visualization in browser...")
    print("   - Walls are rendered as semi-transparent 3D blocks")
    print("   - Orange dots show explored nodes")
    print("   - Blue line shows the final path")
    print("   - Green diamond marks the start")
    print("   - Red diamond marks the goal")
    
    # Show the plot
    fig.show()
    
    print("\n" + "="*70)
    print("🎮 Interactive controls:")
    print("   - Click and drag: Rotate view")
    print("   - Scroll: Zoom in/out")
    print("   - Shift + drag: Pan")
    print("="*70)
    
    return fig


def demo_wall_structure():
    """Demonstrate the wall structure of a single cell"""
    
    print("\n" + "="*70)
    print(" "*15 + "🧱 WALL STRUCTURE DEMO 🧱")
    print("="*70)
    
    # Create tiny maze to show wall structure
    engine = MazeEngine(3, 3, 3)
    engine.generate_maze()
    
    # Check a specific cell
    cell = engine.grid[1][1][1]
    print(f"\n📊 Cell at position (1, 1, 1):")
    print(f"   Wall status:")
    for direction, has_wall in cell.walls.items():
        status = "🧱 WALL" if has_wall else "🚪 OPEN"
        print(f"      {direction:6s}: {status}")
    
    print(f"\n💡 Walls with thickness are positioned between cells:")
    print(f"   - 'east' wall: Located at x=1.5 (between x=1 and x=2)")
    print(f"   - 'north' wall: Located at z=1.5 (between z=1 and z=2)")
    print(f"   - 'up' wall: Located at y=1.5 (between y=1 and y=2)")
    print(f"   - Each wall is a 3D box with configurable thickness")
    
    print("="*70)


def compare_with_without_walls():
    """Compare visualization with and without voxel walls"""
    
    print("\n" + "="*70)
    print(" "*10 + "🎨 COMPARING VISUALIZATIONS 🎨")
    print("="*70)
    
    size = 6
    print(f"\n📦 Generating {size}×{size}×{size} maze...")
    engine = MazeEngine(size, size, size)
    engine.generate_maze()
    
    start = engine.grid[0][0][0]
    goal = engine.grid[size-1][size-1][size-1]
    
    print("🔍 Running pathfinding...")
    path, count, v_len, order = a_star(start, goal, engine)
    
    if not path:
        print("❌ No path found!")
        return
    
    print(f"✅ Path found: {len(path)} steps\n")
    
    # Create both visualizations
    print("Creating visualization WITHOUT voxel walls...")
    fig_no_walls = create_voxel_maze_visualization(
        engine, order, path,
        (0, 0, 0), (size-1, size-1, size-1),
        "Without Voxel Walls",
        show_walls=False
    )
    
    print("Creating visualization WITH voxel walls...")
    fig_with_walls = create_voxel_maze_visualization(
        engine, order, path,
        (0, 0, 0), (size-1, size-1, size-1),
        "With Voxel Walls (Thick Walls)",
        show_walls=True,
        wall_opacity=0.4
    )
    
    print("\n✅ Both visualizations created!")
    print("\n📊 Comparison:")
    print("   WITHOUT walls: Only shows paths and exploration")
    print("   WITH walls: Shows actual maze structure with thick 3D walls")
    
    print("\nOpening WITHOUT voxel walls...")
    fig_no_walls.show()
    
    input("\nPress Enter to view WITH voxel walls...")
    fig_with_walls.show()
    
    print("\n" + "="*70)


if __name__ == "__main__":
    import sys
    
    print("\n🧊 VOXEL MAZE VISUALIZATION DEMO\n")
    print("Choose a demo:")
    print("  1. Full voxel visualization (default)")
    print("  2. Wall structure explanation")
    print("  3. Compare with/without voxel walls")
    print("  4. Run all demos")
    
    choice = input("\nEnter choice (1-4, or Enter for default): ").strip() or "1"
    
    if choice == "1":
        demo_voxel_visualization()
    elif choice == "2":
        demo_wall_structure()
    elif choice == "3":
        compare_with_without_walls()
    elif choice == "4":
        demo_wall_structure()
        input("\nPress Enter to continue to full visualization...")
        demo_voxel_visualization()
        input("\nPress Enter to continue to comparison...")
        compare_with_without_walls()
    else:
        print(f"Invalid choice: {choice}")
        sys.exit(1)
    
    print("\n✨ Demo complete! ✨\n")