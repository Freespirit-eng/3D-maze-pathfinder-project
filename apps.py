"""
Enhanced Streamlit App for 3D Maze Pathfinding Visualization.
Features multiple algorithms, better controls, and improved visualizations.
"""

import streamlit as st
import plotly.graph_objects as go
import time
import numpy as np
from maze_engines import MazeEngine
from pathfinders import a_star, bfs, dijkstra, bidirectional_search
from analytics import Analytics

st.set_page_config(
    page_title="3D Pathfinding Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .algorithm-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = None
if 'analytics' not in st.session_state:
    st.session_state.analytics = Analytics()
if 'race_complete' not in st.session_state:
    st.session_state.race_complete = False
if 'animation_speed' not in st.session_state:
    st.session_state.animation_speed = 0.02

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")

with st.sidebar.expander("🎲 Maze Settings", expanded=True):
    grid_size = st.slider("Grid Size", 5, 30, 15, help="Size of the 3D maze")
    
    maze_algorithm = st.selectbox(
        "Generation Algorithm",
        ["Recursive Backtracking (DFS)", "Kruskal's Algorithm (MST)"],
        help="Algorithm used to generate the maze"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Maze"):
            algo_map = {
                "Recursive Backtracking (DFS)": "recursive_backtracking",
                "Kruskal's Algorithm (MST)": "kruskal"
            }
            st.session_state.engine = MazeEngine(grid_size, grid_size, grid_size)
            st.session_state.engine.generate_maze(
                algorithm=algo_map[maze_algorithm]
            )
            st.session_state.race_complete = False
            st.rerun()
    
    with col2:
        if st.button("📊 Stats"):
            if st.session_state.engine:
                stats = st.session_state.engine.get_maze_stats()
                st.info(f"""
                **Maze Statistics:**
                - Dimensions: {stats['dimensions']}
                - Total cells: {stats['total_cells']}
                - Walls: {stats['total_walls']}
                - Openings: {stats['total_openings']}
                - Algorithm: {stats['algorithm']}
                """)

with st.sidebar.expander("📍 Start & Goal Points", expanded=True):
    col_start, col_goal = st.columns(2)
    with col_start:
        st.markdown("**🟢 Start**")
        start_x = st.number_input("X", 0, grid_size-1, 0, key="start_x")
        start_y = st.number_input("Y", 0, grid_size-1, 0, key="start_y")
        start_z = st.number_input("Z", 0, grid_size-1, 0, key="start_z")
    
    with col_goal:
        st.markdown("**🔴 Goal**")
        goal_x = st.number_input("X", 0, grid_size-1, grid_size-1, key="goal_x")
        goal_y = st.number_input("Y", 0, grid_size-1, grid_size-1, key="goal_y")
        goal_z = st.number_input("Z", 0, grid_size-1, grid_size-1, key="goal_z")

with st.sidebar.expander("🤖 Algorithm Selection", expanded=True):
    algorithms_to_run = st.multiselect(
        "Select Algorithms",
        ["A* (Manhattan)", "A* (Euclidean)", "BFS", "Dijkstra", "Bidirectional BFS"],
        default=["A* (Manhattan)", "BFS"],
        help="Choose which pathfinding algorithms to compare"
    )
    
    if len(algorithms_to_run) > 4:
        st.warning("⚠️ Selecting more than 4 algorithms may slow down visualization")

with st.sidebar.expander("🎬 Animation Settings", expanded=True):
    st.session_state.animation_speed = st.slider(
        "Speed",
        0.001, 0.1, 0.02,
        help="Lower = faster"
    )
    animation_steps = st.slider(
        "Steps",
        10, 100, 30,
        help="More steps = smoother animation"
    )
    show_walls = st.checkbox("Show Walls", value=False, help="Display maze walls")

st.sidebar.divider()

# Analytics
with st.sidebar.expander("📈 Analytics", expanded=False):
    if st.button("📊 View Leaderboard"):
        if st.session_state.analytics.path_history_tree:
            st.session_state.analytics.print_leaderboard(limit=5)
            fastest = st.session_state.analytics.find_fastest_run()
            if fastest:
                st.success(f"🥇 Fastest: {fastest['duration']:.2f}ms ({fastest['algorithm']})")
        else:
            st.info("No data yet. Run some algorithms first!")
    
    if st.button("🗑️ Clear Analytics"):
        st.session_state.analytics.clear_data()
        st.success("Analytics cleared!")

st.sidebar.markdown("### 📖 Legend")
st.sidebar.markdown("""
- 🟦 **Blue**: Final Path
- 🟧 **Orange**: A* Explored
- 🟨 **Yellow**: BFS Explored
- 🟩 **Green**: Dijkstra Explored
- ⬛ **Black**: Walls (if shown)
- 🟢 **Green Marker**: Start
- 🔴 **Red Marker**: Goal
""")

# Helper Functions
def create_3d_plot(engine, visited_nodes, final_path, start, goal, title, 
                  algorithm_color, show_walls=False):
    """Create interactive 3D visualization"""
    fig = go.Figure()
    
    # Draw walls (optional)
    if show_walls:
        wall_coords = []
        for x in range(engine.width):
            for y in range(engine.height):
                for z in range(engine.depth):
                    node = engine.grid[x][y][z]
                    if node.is_wall:
                        wall_coords.append((x, y, z))
        
        if wall_coords:
            wall_x, wall_y, wall_z = zip(*wall_coords)
            fig.add_trace(go.Scatter3d(
                x=wall_x, y=wall_y, z=wall_z,
                mode='markers',
                marker=dict(size=3, color='rgba(0,0,0,0.1)', symbol='square'),
                name='Walls',
                showlegend=False
            ))
    
    # Draw visited nodes
    if visited_nodes:
        vx, vy, vz = zip(*visited_nodes)
        fig.add_trace(go.Scatter3d(
            x=vx, y=vy, z=vz,
            mode='markers',
            marker=dict(size=4, color=algorithm_color, opacity=0.4),
            name='Explored',
            showlegend=True
        ))
    
    # Draw final path
    if final_path:
        px, py, pz = zip(*final_path)
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='lines+markers',
            line=dict(color='blue', width=8),
            marker=dict(size=6, color='blue', symbol='circle'),
            name='Path',
            showlegend=True
        ))
    
    # Mark start and goal
    fig.add_trace(go.Scatter3d(
        x=[start[0]], y=[start[1]], z=[start[2]],
        mode='markers',
        marker=dict(size=12, color='green', symbol='diamond', 
                   line=dict(color='darkgreen', width=2)),
        name='Start',
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter3d(
        x=[goal[0]], y=[goal[1]], z=[goal[2]],
        mode='markers',
        marker=dict(size=12, color='red', symbol='diamond',
                   line=dict(color='darkred', width=2)),
        name='Goal',
        showlegend=True
    ))
    
    # Layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=16, color='#333', family='Arial Black')
        ),
        scene=dict(
            xaxis=dict(showbackground=True, backgroundcolor='rgb(230, 230,230)',
                      gridcolor='white', showticklabels=True, title='X'),
            yaxis=dict(showbackground=True, backgroundcolor='rgb(230, 230,230)',
                      gridcolor='white', showticklabels=True, title='Y'),
            zaxis=dict(showbackground=True, backgroundcolor='rgb(230, 230,230)',
                      gridcolor='white', showticklabels=True, title='Z'),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3)),
            aspectmode='cube'
        ),
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.9)',
                   bordercolor='gray', borderwidth=1)
    )
    
    return fig

def get_algorithm_color(algo_name):
    """Get color for algorithm"""
    colors = {
        'A* (Manhattan)': 'orange',
        'A* (Euclidean)': 'darkorange',
        'BFS': 'gold',
        'Dijkstra': 'limegreen',
        'Bidirectional BFS': 'mediumpurple'
    }
    return colors.get(algo_name, 'gray')

# Main Header
st.markdown('''
    <div class="main-header">
        <h1>🧊 3D Maze Pathfinding Visualizer</h1>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">
            Compare Multiple Pathfinding Algorithms in 3D Space
        </p>
    </div>
''', unsafe_allow_html=True)

# Initialize engine if needed
if st.session_state.engine is None:
    st.session_state.engine = MazeEngine(grid_size, grid_size, grid_size)
    st.session_state.engine.generate_maze()

# Display maze info
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.metric("📏 Maze Size", f"{grid_size}³", help="Cubic dimensions")
with col_info2:
    st.metric("🎯 Total Cells", f"{grid_size**3:,}")
with col_info3:
    if st.session_state.engine:
        stats = st.session_state.engine.get_maze_stats()
        st.metric("🚪 Openings", f"{stats['total_openings']:,}")

# Race button
st.markdown("<br>", unsafe_allow_html=True)
col_center = st.columns([1, 2, 1])[1]
with col_center:
    race_button = st.button("🚀 START PATHFINDING RACE!", use_container_width=True)

if race_button and algorithms_to_run:
    st.session_state.race_complete = False
    
    # Get start and goal nodes
    try:
        start_node = st.session_state.engine.grid[start_x][start_y][start_z]
        goal_node = st.session_state.engine.grid[goal_x][goal_y][goal_z]
    except IndexError:
        st.error("❌ Invalid start or goal coordinates!")
        st.stop()
    
    start_coords = (start_x, start_y, start_z)
    goal_coords = (goal_x, goal_y, goal_z)
    
    # Prepare algorithm functions
    algorithm_funcs = {
        'A* (Manhattan)': lambda s, g, m: a_star(s, g, m, heuristic="manhattan"),
        'A* (Euclidean)': lambda s, g, m: a_star(s, g, m, heuristic="euclidean"),
        'BFS': bfs,
        'Dijkstra': dijkstra,
        'Bidirectional BFS': bidirectional_search
    }
    
    # Run algorithms
    results = {}
    with st.spinner("🔍 Running algorithms..."):
        for algo_name in algorithms_to_run:
            if algo_name in algorithm_funcs:
                st.session_state.engine.reset_pathfinding()
                
                start_time = time.time()
                path, count, v_len, order = algorithm_funcs[algo_name](
                    start_node, goal_node, st.session_state.engine
                )
                duration = (time.time() - start_time) * 1000
                
                results[algo_name] = {
                    'path': path,
                    'count': count,
                    'visited_len': v_len,
                    'order': order,
                    'duration': duration
                }
                
                # Store in analytics
                if path:
                    st.session_state.analytics.insert_into_bst(
                        duration, algo_name,
                        {'nodes_explored': count, 'path_length': len(path)}
                    )
    
    # Create grid layout for visualizations
    num_algos = len(results)
    cols_per_row = 2
    rows_needed = (num_algos + cols_per_row - 1) // cols_per_row
    
    plot_containers = {}
    for i, algo_name in enumerate(results.keys()):
        row = i // cols_per_row
        col = i % cols_per_row
        
        if col == 0:
            cols = st.columns(cols_per_row)
        
        with cols[col]:
            plot_containers[algo_name] = st.empty()
    
    # Animate
    max_steps = max(len(r['order']) for r in results.values())
    step_size = max(1, max_steps // animation_steps)
    
    progress_bar = st.progress(0, text="🏃 Racing...")
    
    for i in range(0, max_steps + step_size, step_size):
        progress = min(i / max_steps, 1.0)
        progress_bar.progress(progress, text=f"Exploring... {int(progress*100)}%")
        
        for algo_name, result in results.items():
            curr_order = result['order'][:min(i, len(result['order']))]
            
            fig = create_3d_plot(
                st.session_state.engine,
                curr_order,
                None,
                start_coords,
                goal_coords,
                f"{algo_name}",
                get_algorithm_color(algo_name),
                show_walls=show_walls
            )
            
            plot_containers[algo_name].plotly_chart(
                fig, use_container_width=True, key=f"{algo_name}_anim_{i}"
            )
        
        time.sleep(st.session_state.animation_speed)
    
    progress_bar.progress(1.0, text="✅ Race complete!")
    
    # Show final results with paths
    for algo_name, result in results.items():
        fig_final = create_3d_plot(
            st.session_state.engine,
            result['order'],
            result['path'],
            start_coords,
            goal_coords,
            f"{algo_name} - Final Result",
            get_algorithm_color(algo_name),
            show_walls=show_walls
        )
        plot_containers[algo_name].plotly_chart(
            fig_final, use_container_width=True, key=f"{algo_name}_final"
        )
    
    # Performance comparison
    st.divider()
    st.markdown("## 📊 Performance Comparison")
    
    # Metrics
    metric_cols = st.columns(len(results))
    for idx, (algo_name, result) in enumerate(results.items()):
        with metric_cols[idx]:
            st.markdown(f"### {algo_name}")
            if result['path']:
                st.metric("⏱️ Time", f"{result['duration']:.2f}ms")
                st.metric("🔍 Nodes", f"{result['visited_len']}")
                st.metric("📏 Path", f"{len(result['path'])}")
                efficiency = (len(result['path']) / result['visited_len'] * 100)
                st.metric("🎯 Efficiency", f"{efficiency:.1f}%")
            else:
                st.error("No path found")
    
    # Comparison table
    st.markdown("### Detailed Comparison")
    
    successful_results = {k: v for k, v in results.items() if v['path']}
    
    if successful_results:
        comparison_data = []
        for algo_name, result in successful_results.items():
            comparison_data.append({
                "Algorithm": algo_name,
                "Time (ms)": f"{result['duration']:.2f}",
                "Nodes Explored": result['visited_len'],
                "Path Length": len(result['path']),
                "Efficiency": f"{(len(result['path']) / result['visited_len'] * 100):.1f}%"
            })
        
        st.dataframe(comparison_data, use_container_width=True)
        
        # Determine winners
        fastest = min(successful_results.items(), key=lambda x: x[1]['duration'])
        most_efficient = max(successful_results.items(),
                            key=lambda x: len(x[1]['path']) / x[1]['visited_len'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"⚡ **Fastest**: {fastest[0]} ({fastest[1]['duration']:.2f}ms)")
        with col2:
            eff = len(most_efficient[1]['path']) / most_efficient[1]['visited_len'] * 100
            st.success(f"🎯 **Most Efficient**: {most_efficient[0]} ({eff:.1f}%)")
    
    st.session_state.race_complete = True
    st.balloons()

elif race_button and not algorithms_to_run:
    st.warning("⚠️ Please select at least one algorithm to run!")

# Info section
if not st.session_state.race_complete:
    st.info("👆 Configure your maze and select algorithms, then click 'START PATHFINDING RACE!'")
    
    with st.expander("ℹ️ About the Algorithms"):
        st.markdown("""
        ### Available Pathfinding Algorithms:
        
        **🔷 A* Search (A-Star)**
        - Uses heuristic to estimate distance to goal
        - Manhattan: Sum of absolute differences in coordinates
        - Euclidean: Straight-line distance
        - Most efficient for grid-based pathfinding
        
        **🔶 BFS (Breadth-First Search)**
        - Explores all nodes at current depth before going deeper
        - No heuristic guidance
        - Guarantees shortest path
        
        **🔷 Dijkstra's Algorithm**
        - Similar to A* but without heuristic
        - Uniform cost search
        - Guaranteed shortest path
        
        **🔶 Bidirectional BFS**
        - Searches from both start and goal simultaneously
        - Can be faster than regular BFS
        - Good for long paths
        
        ### Maze Generation:
        
        **Recursive Backtracking (DFS)**
        - Creates long, winding corridors
        - Perfect mazes (one path between any two points)
        - More challenging to solve
        
        **Kruskal's Algorithm (MST)**
        - Creates more open spaces
        - Uses minimum spanning tree approach
        - Different maze characteristics
        """)
