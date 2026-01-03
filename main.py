"""
Main entry point for 3D Maze Pathfinding Comparison.
Command-line interface with multiple algorithm support.
"""

import time
import sys
from maze_engines import MazeEngine
from pathfinders import a_star, bfs, dijkstra, bidirectional_search
from analytics import Analytics


def print_header():
    """Print fancy header"""
    print("\n" + "="*80)
    print(" "*20 + "🎮 3D MAZE PATHFINDING COMPARISON 🎮")
    print("="*80 + "\n")


def print_section(title):
    """Print section divider"""
    print("\n" + "-"*80)
    print(f"  {title}")
    print("-"*80)


def run_algorithm(algorithm_func, name, start, goal, engine, analytics, color_code=""):
    """Run a single pathfinding algorithm and collect results"""
    print(f"\n{color_code}🔍 Running {name}...")
    
    start_time = time.time()
    result = algorithm_func(start, goal, engine)
    end_time = time.time()
    
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    
    if result[0] is not None:  # Path found
        path, nodes_explored, visited_count, visited_order = result
        path_length = len(path)
        
        # Store in analytics
        metadata = {
            'nodes_explored': nodes_explored,
            'path_length': path_length,
            'visited_count': visited_count
        }
        analytics.insert_into_bst(duration, name, metadata)
        
        print(f"✅ {name} completed successfully!")
        print(f"   ⏱️  Time: {duration:.2f} ms")
        print(f"   🔍 Nodes explored: {nodes_explored}")
        print(f"   📏 Path length: {path_length} steps")
        print(f"   📊 Efficiency: {(path_length / nodes_explored * 100):.1f}%")
        
        return {
            'algorithm': name,
            'duration': duration,
            'nodes_explored': nodes_explored,
            'path_length': path_length,
            'visited_count': visited_count,
            'success': True
        }
    else:
        print(f"❌ {name}: No path found")
        return {
            'algorithm': name,
            'duration': duration,
            'success': False
        }


def run_comparison(maze_size=30, runs=1, algorithms=None):
    """
    Run pathfinding comparison with multiple algorithms.
    
    Args:
        maze_size: Size of the 3D maze (creates size×size×size maze)
        runs: Number of times to run the comparison
        algorithms: List of algorithm names to test (None = all)
    """
    print_header()
    
    # Initialize analytics
    analytics = Analytics()
    
    # Algorithm configurations
    all_algorithms = [
        (a_star, "A* (Manhattan)", "\033[94m"),      # Blue
        (bfs, "BFS", "\033[93m"),                     # Yellow
        (dijkstra, "Dijkstra", "\033[92m"),          # Green
        (bidirectional_search, "Bidirectional BFS", "\033[95m")  # Magenta
    ]
    
    # Filter algorithms if specified
    if algorithms:
        all_algorithms = [(func, name, color) for func, name, color in all_algorithms 
                         if name in algorithms or name.lower() in algorithms]
    
    # Run multiple times if requested
    for run_num in range(1, runs + 1):
        if runs > 1:
            print_section(f"RUN {run_num}/{runs}")
        
        # Initialize maze engine
        print(f"🎲 Generating {maze_size}×{maze_size}×{maze_size} maze...")
        engine = MazeEngine(maze_size, maze_size, maze_size)
        engine.generate_maze(algorithm="recursive_backtracking")
        
        # Display maze stats
        stats = engine.get_maze_stats()
        print(f"✅ Maze generated using {stats['algorithm']}")
        print(f"   📦 Total cells: {stats['total_cells']}")
        print(f"   🧱 Total walls: {stats['total_walls']}")
        print(f"   🚪 Total openings: {stats['total_openings']}")
        
        # Set start and goal
        start = engine.grid[0][0][0]
        goal = engine.grid[maze_size-1][maze_size-1][maze_size-1]
        
        # Ensure start and goal are not walls
        start.is_wall = False
        goal.is_wall = False
        
        print(f"\n📍 Start: ({start.x}, {start.y}, {start.z})")
        print(f"🎯 Goal:  ({goal.x}, {goal.y}, {goal.z})")
        
        print_section("PATHFINDING ALGORITHMS")
        
        # Run each algorithm
        results = []
        for algorithm_func, algorithm_name, color_code in all_algorithms:
            result = run_algorithm(
                algorithm_func, algorithm_name, start, goal, 
                engine, analytics, color_code
            )
            results.append(result)
            
            # Reset pathfinding state between algorithms
            engine.reset_pathfinding()
        
        # Print comparison for this run
        print_section(f"COMPARISON - Run {run_num}")
        
        successful_results = [r for r in results if r['success']]
        
        if successful_results:
            print(f"\n{'Algorithm':<25} | {'Time (ms)':>12} | {'Nodes':>8} | "
                  f"{'Path':>6} | {'Efficiency':>10}")
            print("-"*80)
            
            # Sort by time
            for result in sorted(successful_results, key=lambda x: x['duration']):
                efficiency = (result['path_length'] / result['nodes_explored'] * 100)
                print(f"{result['algorithm']:<25} | {result['duration']:>11.2f} | "
                      f"{result['nodes_explored']:>8} | {result['path_length']:>6} | "
                      f"{efficiency:>9.1f}%")
            
            # Find winner
            fastest = min(successful_results, key=lambda x: x['duration'])
            most_efficient = max(successful_results, 
                                key=lambda x: x['path_length']/x['nodes_explored'])
            
            print("\n🏆 Winners:")
            print(f"   ⚡ Fastest: {fastest['algorithm']} ({fastest['duration']:.2f} ms)")
            print(f"   🎯 Most Efficient: {most_efficient['algorithm']} "
                  f"({most_efficient['path_length']}/{most_efficient['nodes_explored']} = "
                  f"{most_efficient['path_length']/most_efficient['nodes_explored']*100:.1f}%)")
    
    # Final statistics if multiple runs
    if runs > 1:
        print_section("OVERALL STATISTICS")
        analytics.print_algorithm_comparison()
    
    # Print leaderboard
    analytics.print_leaderboard(limit=10)
    
    # Print fastest run
    fastest_run = analytics.find_fastest_run()
    if fastest_run:
        print(f"\n🥇 All-time fastest: {fastest_run['duration']:.2f} ms "
              f"({fastest_run['algorithm']})")
    
    print("\n" + "="*80)
    print(" "*25 + "🎮 Comparison Complete! 🎮")
    print("="*80 + "\n")


def interactive_mode():
    """Interactive mode for custom maze configuration"""
    print_header()
    print("🎮 Interactive Maze Solver")
    print("\nConfigure your maze parameters:\n")
    
    try:
        size = int(input("Enter maze size (5-50, default 30): ") or "30")
        size = max(5, min(50, size))
        
        runs = int(input("Number of runs (1-10, default 1): ") or "1")
        runs = max(1, min(10, runs))
        
        print("\nAvailable algorithms:")
        print("  1. A* (Manhattan)")
        print("  2. BFS")
        print("  3. Dijkstra")
        print("  4. Bidirectional BFS")
        print("  5. All algorithms")
        
        choice = input("\nSelect algorithms (1-5, default 5): ") or "5"
        
        if choice == "5":
            algorithms = None  # Run all
        else:
            algo_map = {
                "1": ["A* (Manhattan)"],
                "2": ["BFS"],
                "3": ["Dijkstra"],
                "4": ["Bidirectional BFS"]
            }
            algorithms = algo_map.get(choice, None)
        
        run_comparison(maze_size=size, runs=runs, algorithms=algorithms)
        
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="3D Maze Pathfinding Comparison Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--size', '-s',
        type=int,
        default=30,
        help='Size of the 3D maze (default: 30)'
    )
    
    parser.add_argument(
        '--runs', '-r',
        type=int,
        default=1,
        help='Number of comparison runs (default: 1)'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--algorithms', '-a',
        nargs='+',
        choices=['astar', 'bfs', 'dijkstra', 'bidirectional'],
        help='Specific algorithms to run'
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    else:
        # Map short names to full names
        algo_map = {
            'astar': 'A* (Manhattan)',
            'bfs': 'BFS',
            'dijkstra': 'Dijkstra',
            'bidirectional': 'Bidirectional BFS'
        }
        algorithms = [algo_map[a] for a in args.algorithms] if args.algorithms else None
        
        run_comparison(maze_size=args.size, runs=args.runs, algorithms=algorithms)
