"""
Enhanced Streamlit App with Voxel-Style 3D Maze Visualization.
Renders walls as actual 3D blocks/voxels.
"""

import streamlit as st
import time
from maze_engines import MazeEngine
from pathfinders import a_star, bfs, dijkstra, bidirectional_search
from analytics import Analytics
from voxel_visualizer import create_voxel_maze_visualization

st.set_page_config(
    page_title="3D Voxel Maze Visualizer",
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
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = None
if 'analytics' not in st.session_state:
    st.session_state.analytics = Analytics()
if 'race_complete' not in st.session_state:
    st.session_state.race_complete = False
if 'show_animation' not in st.session_state:
    st.session_state.show_animation = True

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")

with st.sidebar.expander("🎲 Maze Settings", expanded=True):
    grid_size = st.slider("Grid Size", 5, 15, 8, 
                         help="Larger mazes take longer to render with voxel walls")
    
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
    algorithm_choice = st.selectbox(
        "Select Algorithm",
        ["A* (Manhattan)", "A* (Euclidean)", "BFS", "Dijkstra", "Bidirectional BFS"],
        help="Choose pathfinding algorithm to visualize"
    )

with st.sidebar.expander("🎨 Visualization Settings", expanded=True):
    show_voxel_walls = st.checkbox("Show Voxel Walls", value=True,
                                   help="Render walls as 3D blocks (may be slow for large mazes)")
    wall_opacity = st.slider("Wall Opacity", 0.0, 1.0, 0.3, 0.05,
                            help="Transparency of wall voxels")
    wall_color = st.selectbox("Wall Color", 
                             ["gray", "darkgray", "black", "brown", "dimgray"],
                             help="Color of wall voxels")
    
    st.session_state.show_animation = st.checkbox("Show Animation", value=True,
                                                  help="Animate the pathfinding process")
    
    if st.session_state.show_animation:
        animation_speed = st.slider("Animation Speed", 0.001, 0.1, 0.03,
                                   help="Lower = faster")
        animation_steps = st.slider("Animation Steps", 5, 50, 20,
                                   help="More steps = smoother but slower")

st.sidebar.divider()

with st.sidebar.expander("📈 Analytics", expanded=False):
    if st.button("📊 View Stats"):
        if st.session_state.analytics.path_history_tree:
            summary = st.session_state.analytics.get_algorithm_summary()
            for algo, stats in summary.items():
                st.write(f"**{algo}**")
                st.write(f"- Runs: {stats['runs']}")
                st.write(f"- Avg Time: {stats['avg_time']:.2f}ms")
                st.write(f"- Best: {stats['best_time']:.2f}ms")
        else:
            st.info("No data yet!")
    
    if st.button("🗑️ Clear Analytics"):
        st.session_state.analytics.clear_data()
        st.success("Cleared!")

st.sidebar.markdown("### 📖 About Voxel Rendering")
st.sidebar.markdown("""
Voxel walls are rendered as 3D blocks positioned between cells. 
Each wall has physical thickness and proper 3D structure.

**Note**: Large mazes (>15×15×15) may render slowly due to the number of wall voxels.
""")

# Main Header
st.markdown('''
    <div class="main-header">
        <h1>🧊 3D Voxel Maze Visualizer</h1>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">
            Pathfinding with Thick Voxel Walls
        </p>
    </div>
''', unsafe_allow_html=True)

# Initialize engine if needed
if st.session_state.engine is None:
    with st.spinner("Generating initial maze..."):
        st.session_state.engine = MazeEngine(grid_size, grid_size, grid_size)
        st.session_state.engine.generate_maze()

# Display maze info
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.metric("📏 Maze Size", f"{grid_size}³ voxels")
with col_info2:
    st.metric("🎯 Total Cells", f"{grid_size**3:,}")
with col_info3:
    if st.session_state.engine:
        stats = st.session_state.engine.get_maze_stats()
        st.metric("🧱 Walls", f"{stats['total_walls']:,}")

# Main action button
st.markdown("<br>", unsafe_allow_html=True)
col_center = st.columns([1, 2, 1])[1]
with col_center:
    run_button = st.button(f"🚀 RUN {algorithm_choice}!", use_container_width=True)

if run_button:
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
    
    # Map algorithm choice to function
    algorithm_map = {
        'A* (Manhattan)': lambda s, g, m: a_star(s, g, m, heuristic="manhattan"),
        'A* (Euclidean)': lambda s, g, m: a_star(s, g, m, heuristic="euclidean"),
        'BFS': bfs,
        'Dijkstra': dijkstra,
        'Bidirectional BFS': bidirectional_search
    }
    
    # Run algorithm
    algo_func = algorithm_map[algorithm_choice]
    
    with st.spinner(f"🔍 Running {algorithm_choice}..."):
        st.session_state.engine.reset_pathfinding()
        
        start_time = time.time()
        path, count, v_len, order = algo_func(start_node, goal_node, st.session_state.engine)
        duration = (time.time() - start_time) * 1000
    
    # Display results
    st.markdown("---")
    st.markdown(f"## 🎯 {algorithm_choice} Results")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⏱️ Time", f"{duration:.2f}ms")
    with col2:
        st.metric("🔍 Nodes Explored", f"{v_len:,}")
    with col3:
        if path:
            st.metric("📏 Path Length", f"{len(path)}")
        else:
            st.metric("📏 Path Length", "No path")
    with col4:
        if path:
            efficiency = (len(path) / v_len * 100)
            st.metric("🎯 Efficiency", f"{efficiency:.1f}%")
        else:
            st.metric("🎯 Efficiency", "N/A")
    
    # Store in analytics
    if path:
        st.session_state.analytics.insert_into_bst(
            duration, algorithm_choice,
            {'nodes_explored': count, 'path_length': len(path)}
        )
    
    # Visualization
    st.markdown("### 🧊 3D Voxel Visualization")
    
    if show_voxel_walls and grid_size > 15:
        st.warning("⚠️ Large mazes with voxel walls may take a while to render. Consider disabling voxel walls or using a smaller maze.")
    
    viz_container = st.empty()
    
    if st.session_state.show_animation and path:
        # Animated visualization
        progress_bar = st.progress(0, text="🏃 Animating pathfinding...")
        
        max_steps = len(order)
        step_size = max(1, max_steps // animation_steps)
        
        for i in range(0, max_steps + step_size, step_size):
            progress = min(i / max_steps, 1.0)
            progress_bar.progress(progress, text=f"Exploring... {int(progress*100)}%")
            
            curr_order = order[:min(i, len(order))]
            
            # Show path only at the end
            show_path = path if i >= max_steps else None
            
            fig = create_voxel_maze_visualization(
                st.session_state.engine,
                visited_nodes=curr_order,
                final_path=show_path,
                start=start_coords,
                goal=goal_coords,
                title=f"{algorithm_choice} - Exploring",
                show_walls=show_voxel_walls,
                wall_opacity=wall_opacity,
                wall_color=wall_color
            )
            
            viz_container.plotly_chart(fig, use_container_width=True, key=f"anim_{i}")
            
            if i < max_steps:  # Don't sleep on last frame
                time.sleep(animation_speed)
        
        progress_bar.progress(1.0, text="✅ Complete!")
    
    else:
        # Static final visualization
        with st.spinner("Rendering voxel maze..."):
            fig = create_voxel_maze_visualization(
                st.session_state.engine,
                visited_nodes=order,
                final_path=path,
                start=start_coords,
                goal=goal_coords,
                title=f"{algorithm_choice} - Final Result",
                show_walls=show_voxel_walls,
                wall_opacity=wall_opacity,
                wall_color=wall_color
            )
            
            viz_container.plotly_chart(fig, use_container_width=True)
    
    # Success message
    if path:
        st.success(f"✅ Path found! {algorithm_choice} explored {v_len:,} nodes to find a path of length {len(path)}.")
    else:
        st.error(f"❌ No path found between start and goal.")
    
    st.session_state.race_complete = True

# Info section
if not st.session_state.race_complete:
    st.info("👆 Configure your maze and select an algorithm, then click 'RUN' to visualize pathfinding with voxel walls!")
    
    with st.expander("ℹ️ About Voxel Visualization"):
        st.markdown("""
        ### What are Voxel Walls?
        
        Unlike traditional maze visualizations that show walls as simple obstacles, 
        this app renders walls as **3D voxels (volumetric pixels)** - actual blocks 
        with thickness and volume.
        
        ### Features:
        
        **🧱 Thick Walls**
        - Each wall has physical thickness
        - Positioned between adjacent cells
        - Proper 3D structure with all 6 faces
        
        **🎨 Customizable Appearance**
        - Adjustable opacity
        - Multiple color options
        - Can be toggled on/off
        
        **⚡ Performance**
        - Smaller mazes (5-10): Very fast
        - Medium mazes (10-15): Good performance
        - Large mazes (>15): May be slow to render
        
        ### How It Works:
        
        Each node in the maze tracks walls in 6 directions (north, south, east, 
        west, up, down). When visualizing, the app creates 3D mesh geometry for 
        each wall, positioned precisely between cells.
        
        This creates a true voxel-style visualization suitable for:
        - Game engine integration
        - 3D printing
        - Virtual reality
        - Realistic maze rendering
        """)
    
    with st.expander("🎮 Tips for Best Results"):
        st.markdown("""
        **For Fast Rendering:**
        - Use maze sizes 8-12
        - Disable voxel walls for quick tests
        - Reduce wall opacity
        
        **For Best Visuals:**
        - Use maze sizes 10-15
        - Enable voxel walls
        - Try different wall colors
        - Adjust camera angle by dragging
        
        **For Performance Testing:**
        - Disable animation
        - Disable voxel walls
        - Use larger mazes (15-20)
        - Check analytics for statistics
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>3D Voxel Maze Visualizer</strong> | Recursive Backtracking (DFS) | Thick Wall Rendering</p>
        <p>Interact with the 3D plot: Click and drag to rotate, scroll to zoom, shift+drag to pan</p>
    </div>
""", unsafe_allow_html=True)