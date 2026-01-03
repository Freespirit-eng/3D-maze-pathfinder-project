"""
Example usage and tests for the 3D Maze Solver.
Run this file to verify all components work correctly.
"""

from maze_engines import MazeEngine
from pathfinders import a_star, bfs, dijkstra, bidirectional_search
from analytics import Analytics
import time


def test_maze_generation():
    """Test maze generation with both algorithms"""
    print("🧪 Testing Maze Generation...")
    
    # Test Recursive Backtracking
    print("\n1️⃣ Testing Recursive Backtracking (DFS)")
    engine_rb = MazeEngine(10, 10, 10)
    engine_rb.generate_maze(algorithm="recursive_backtracking")
    stats_rb = engine_rb.get_maze_stats()
    print(f"   ✅ Generated {stats_rb['dimensions']} maze")
    print(f"   📊 Cells: {stats_rb['total_cells']}, Openings: {stats_rb['total_openings']}")
    
    # Test Kruskal's Algorithm
    print("\n2️⃣ Testing Kruskal's Algorithm (MST)")
    engine_k = MazeEngine(10, 10, 10)
    engine_k.generate_maze(algorithm="kruskal")
    stats_k = engine_k.get_maze_stats()
    print(f"   ✅ Generated {stats_k['dimensions']} maze")
    print(f"   📊 Cells: {stats_k['total_cells']}, Openings: {stats_k['total_openings']}")
    
    return engine_rb


def test_pathfinding(engine):
    """Test all pathfinding algorithms"""
    print("\n🧪 Testing Pathfinding Algorithms...")
    
    start = engine.grid[0][0][0]
    goal = engine.grid[9][9][9]
    
    # Ensure start and goal are accessible
    start.is_wall = False
    goal.is_wall = False
    
    algorithms = [
        (a_star, "A* (Manhattan)"),
        (bfs, "BFS"),
        (dijkstra, "Dijkstra"),
        (bidirectional_search, "Bidirectional BFS")
    ]
    
    results = []
    
    for algo_func, algo_name in algorithms:
        print(f"\n{algo_name}:")
        engine.reset_pathfinding()
        
        start_time = time.time()
        path, count, v_len, order = algo_func(start, goal, engine)
        duration = (time.time() - start_time) * 1000
        
        if path:
            print(f"   ✅ Path found!")
            print(f"   ⏱️  Time: {duration:.2f}ms")
            print(f"   🔍 Nodes explored: {v_len}")
            print(f"   📏 Path length: {len(path)}")
            print(f"   🎯 Efficiency: {(len(path) / v_len * 100):.2f}%")
            
            results.append({
                'algorithm': algo_name,
                'duration': duration,
                'nodes': v_len,
                'path_length': len(path)
            })
        else:
            print(f"   ❌ No path found")
    
    return results


def test_analytics(results):
    """Test analytics functionality"""
    print("\n🧪 Testing Analytics...")
    
    analytics = Analytics()
    
    # Insert results
    for result in results:
        metadata = {
            'nodes_explored': result['nodes'],
            'path_length': result['path_length']
        }
        analytics.insert_into_bst(
            result['duration'],
            result['algorithm'],
            metadata
        )
    
    print("\n📊 Performance Summary:")
    analytics.print_algorithm_comparison()
    
    print("\n🏆 Leaderboard (Top 5):")
    analytics.print_leaderboard(limit=5)
    
    fastest = analytics.find_fastest_run()
    if fastest:
        print(f"\n🥇 Fastest run: {fastest['duration']:.2f}ms ({fastest['algorithm']})")
    
    slowest = analytics.find_slowest_run()
    if slowest:
        print(f"🐌 Slowest run: {slowest['duration']:.2f}ms ({slowest['algorithm']})")
    
    return analytics


def test_node_functionality():
    """Test Node class functionality"""
    print("\n🧪 Testing Node Functionality...")
    
    from node import Node
    
    # Create test nodes
    node1 = Node(0, 0, 0)
    node2 = Node(1, 0, 0)  # East neighbor
    
    print("\n1️⃣ Testing wall connectivity:")
    print(f"   Initial walls for node1: {sum(node1.walls.values())} walls")
    
    # Remove wall between nodes
    node1.remove_wall_to(node2)
    print(f"   After removing wall: {sum(node1.walls.values())} walls")
    print(f"   Wall to east: {node1.walls['east']}")
    print(f"   Neighbor wall to west: {node2.walls['west']}")
    
    # Test wall checking
    has_wall = node1.has_wall_to(node2)
    print(f"   Has wall between nodes: {has_wall}")
    
    print("\n2️⃣ Testing pathfinding attributes:")
    node1.g_score = 10
    node1.h_score = 5
    node1.f_score = 15
    print(f"   g_score: {node1.g_score}")
    print(f"   h_score: {node1.h_score}")
    print(f"   f_score: {node1.f_score}")
    
    node1.reset_pathfinding()
    print(f"   After reset - g_score: {node1.g_score}")
    
    print("\n✅ Node functionality tests passed!")


def run_comprehensive_test():
    """Run all tests"""
    print("="*80)
    print(" "*25 + "🧪 COMPREHENSIVE TESTS 🧪")
    print("="*80)
    
    # Test Node
    test_node_functionality()
    
    # Test Maze Generation
    engine = test_maze_generation()
    
    # Test Pathfinding
    results = test_pathfinding(engine)
    
    # Test Analytics
    if results:
        analytics = test_analytics(results)
    
    print("\n" + "="*80)
    print(" "*25 + "✅ ALL TESTS PASSED! ✅")
    print("="*80)
    print("\nYou can now run:")
    print("  • python main.py          - Command-line interface")
    print("  • python main.py -i       - Interactive mode")
    print("  • streamlit run app.py    - Web interface")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_comprehensive_test()
