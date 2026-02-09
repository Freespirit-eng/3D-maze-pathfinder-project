"""
3D Maze Pathfinder - Clean & Modern Streamlit App
"""

import streamlit as st
import time
from maze_engines import MazeEngine
from pathfinders import a_star, bfs, dijkstra
from analytics import Analytics
from voxel_visualizer import create_voxel_maze_visualization

st.set_page_config(
    page_title="3D Maze Pathfinder",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Elegant CSS Theme - Soft Purple Palette
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 50%, #12121f 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(18, 18, 30, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(155, 140, 216, 0.15);
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #b8b8d0 !important;
    }
    
    /* Main header - soft purple gradient */
    .main-header {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(135deg, #7c6bb8 0%, #9b8cd8 50%, #a89ed4 100%);
        color: white;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(124, 107, 184, 0.25);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -1px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Buttons - soft purple */
    .stButton>button {
        background: linear-gradient(135deg, #7c6bb8 0%, #9b8cd8 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(124, 107, 184, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(155, 140, 216, 0.4);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #c4b8e8;
        font-size: 1.6rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888899;
        font-weight: 500;
    }
    
    /* Text styling */
    .stMarkdown, .stText, h1, h2, h3, p {
        color: #d0d0e0;
    }
    
    h2 {
        font-weight: 600;
        color: #c4b8e8;
    }
    
    /* Success message */
    .stSuccess {
        background: rgba(120, 180, 120, 0.12);
        border: 1px solid rgba(120, 180, 120, 0.35);
    }
    
    /* Info message */
    .stInfo {
        background: rgba(155, 140, 216, 0.12);
        border: 1px solid rgba(155, 140, 216, 0.35);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        color: #b8c5d6 !important;
        background: rgba(30, 30, 60, 0.6);
        border-radius: 10px;
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 12px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(100, 120, 255, 0.2);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00d4aa, #00b4d8);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = None
if 'analytics' not in st.session_state:
    st.session_state.analytics = Analytics()
if 'race_complete' not in st.session_state:
    st.session_state.race_complete = False

# Sidebar Configuration
st.sidebar.title("Settings")

# Maze Settings
st.sidebar.subheader("Maze")
grid_size = st.sidebar.slider("Grid Size", 5, 15, 8)

maze_algorithm = st.sidebar.selectbox(
    "Generation",
    ["Recursive Backtracking", "Kruskal's Algorithm"]
)

if st.sidebar.button("Generate New Maze", use_container_width=True):
    algo_map = {
        "Recursive Backtracking": "recursive_backtracking",
        "Kruskal's Algorithm": "kruskal"
    }
    st.session_state.engine = MazeEngine(grid_size, grid_size, grid_size)
    st.session_state.engine.generate_maze(algorithm=algo_map[maze_algorithm])
    st.session_state.race_complete = False
    st.rerun()

st.sidebar.divider()

# Start & Goal
st.sidebar.subheader("Start & Goal")
col_s, col_g = st.sidebar.columns(2)
with col_s:
    st.markdown("**Start**")
    start_x = st.number_input("X", 0, grid_size-1, 0, key="sx")
    start_y = st.number_input("Y", 0, grid_size-1, 0, key="sy")
    start_z = st.number_input("Z", 0, grid_size-1, 0, key="sz")
with col_g:
    st.markdown("**Goal**")
    goal_x = st.number_input("X", 0, grid_size-1, grid_size-1, key="gx")
    goal_y = st.number_input("Y", 0, grid_size-1, grid_size-1, key="gy")
    goal_z = st.number_input("Z", 0, grid_size-1, grid_size-1, key="gz")

st.sidebar.divider()

# Algorithm
st.sidebar.subheader("Algorithm")
algorithm_choice = st.sidebar.selectbox(
    "Pathfinding",
    ["A*", "BFS", "Dijkstra"]
)

st.sidebar.divider()

# Visualization
st.sidebar.subheader("Display")
show_walls = st.sidebar.checkbox("Show Walls", value=True)
wall_opacity = st.sidebar.slider("Wall Opacity", 0.1, 0.5, 0.25)
show_animation = st.sidebar.checkbox("Animate", value=True)

st.sidebar.divider()

# Analytics Section
with st.sidebar.expander("Analytics", expanded=False):
    if st.session_state.analytics.path_history_tree:
        summary = st.session_state.analytics.get_algorithm_summary()
        for algo, stats in summary.items():
            st.markdown(f"**{algo}**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Runs: {stats['runs']}")
                st.write(f"Avg: {stats['avg_time']:.1f}ms")
            with col2:
                st.write(f"Best: {stats['best_time']:.1f}ms")
                st.write(f"Worst: {stats['worst_time']:.1f}ms")
            st.divider()
        
        if st.button("Clear All Stats"):
            st.session_state.analytics.clear_data()
            st.rerun()
    else:
        st.info("No data yet. Run an algorithm to see stats!")

# Main Header
st.markdown('''
    <div class="main-header">
        <h1>3D Maze Pathfinder</h1>
    </div>
''', unsafe_allow_html=True)

# Initialize engine if needed
if st.session_state.engine is None:
    with st.spinner("Generating maze..."):
        st.session_state.engine = MazeEngine(grid_size, grid_size, grid_size)
        st.session_state.engine.generate_maze()

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Size", f"{grid_size}×{grid_size}×{grid_size}")
with col2:
    st.metric("Cells", f"{grid_size**3}")
with col3:
    stats = st.session_state.engine.get_maze_stats()
    st.metric("Walls", stats['total_walls'])

# Run button
st.markdown("")
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    run_button = st.button(f"▶ RUN {algorithm_choice}", use_container_width=True)

if run_button:
    st.session_state.race_complete = False
    
    try:
        start_node = st.session_state.engine.grid[start_x][start_y][start_z]
        goal_node = st.session_state.engine.grid[goal_x][goal_y][goal_z]
    except IndexError:
        st.error("Invalid coordinates!")
        st.stop()
    
    start_coords = (start_x, start_y, start_z)
    goal_coords = (goal_x, goal_y, goal_z)
    
    algorithm_map = {
        'A*': lambda s, g, m: a_star(s, g, m, heuristic="manhattan"),
        'BFS': bfs,
        'Dijkstra': dijkstra
    }
    
    algo_func = algorithm_map[algorithm_choice]
    
    with st.spinner(f"Running {algorithm_choice}..."):
        st.session_state.engine.reset_pathfinding()
        start_time = time.time()
        path, count, v_len, order = algo_func(start_node, goal_node, st.session_state.engine)
        duration = (time.time() - start_time) * 1000
    
    # Results
    st.markdown("---")
    st.markdown(f"## Results")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Time", f"{duration:.1f}ms")
    with col2:
        st.metric("Explored", f"{v_len}")
    with col3:
        st.metric("Path Length", len(path) if path else "N/A")
    with col4:
        if path and v_len > 0:
            eff = (len(path) / v_len * 100)
            st.metric("Efficiency", f"{eff:.1f}%")
        else:
            st.metric("Efficiency", "N/A")
    
    # Store in analytics
    if path:
        st.session_state.analytics.insert_into_bst(
            duration, algorithm_choice,
            {'nodes_explored': count, 'path_length': len(path)}
        )
    
    # Visualization
    st.markdown("### 3D Visualization")
    viz_container = st.empty()
    
    if show_animation and path:
        progress = st.progress(0)
        
        # Step 1: Initial
        progress.progress(20, "Initializing...")
        fig = create_voxel_maze_visualization(
            st.session_state.engine,
            visited_nodes=None, final_path=None,
            start=start_coords, goal=goal_coords,
            title=f"{algorithm_choice}",
            show_walls=show_walls, wall_opacity=wall_opacity, wall_color="gray"
        )
        viz_container.plotly_chart(fig, use_container_width=True, key="v1")
        time.sleep(0.4)
        
        # Step 2: Explored
        progress.progress(60, "Exploring...")
        fig = create_voxel_maze_visualization(
            st.session_state.engine,
            visited_nodes=order, final_path=None,
            start=start_coords, goal=goal_coords,
            title=f"{algorithm_choice} - Explored {len(order)} nodes",
            show_walls=show_walls, wall_opacity=wall_opacity, wall_color="gray"
        )
        viz_container.plotly_chart(fig, use_container_width=True, key="v2")
        time.sleep(0.5)
        
        # Step 3: Final
        progress.progress(100, "Done!")
        fig = create_voxel_maze_visualization(
            st.session_state.engine,
            visited_nodes=order, final_path=path,
            start=start_coords, goal=goal_coords,
            title=f"{algorithm_choice} - Path Found!",
            show_walls=show_walls, wall_opacity=wall_opacity, wall_color="gray"
        )
        viz_container.plotly_chart(fig, use_container_width=True, key="v3")
    else:
        fig = create_voxel_maze_visualization(
            st.session_state.engine,
            visited_nodes=order, final_path=path,
            start=start_coords, goal=goal_coords,
            title=f"{algorithm_choice} - Result",
            show_walls=show_walls, wall_opacity=wall_opacity, wall_color="gray"
        )
        viz_container.plotly_chart(fig, use_container_width=True)
    
    if path:
        st.success(f"✓ Path found! Length: {len(path)}, Nodes explored: {v_len}")
    else:
        st.error("✗ No path found")
    
    st.session_state.race_complete = True

# Initial info
if not st.session_state.race_complete:
    st.info("Click **RUN** to start pathfinding visualization")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem;'>
    Drag to rotate • Scroll to zoom • Shift+drag to pan
</div>
""", unsafe_allow_html=True)