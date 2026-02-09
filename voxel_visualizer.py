"""
Enhanced 3D Maze Visualization with better animations and maze appearance.
Renders walls as wireframe cubes and shows smooth path animations.
"""

import plotly.graph_objects as go
import numpy as np


def create_wireframe_edges(x, y, z, size=1.0):
    """
    Create wireframe edges for a cube positioned at (x, y, z).
    Returns x, y, z coordinates for drawing lines.
    """
    s = size / 2
    # Define the 8 vertices of a cube centered at (x, y, z)
    vertices = [
        (x-s, y-s, z-s), (x+s, y-s, z-s), (x+s, y+s, z-s), (x-s, y+s, z-s),  # bottom
        (x-s, y-s, z+s), (x+s, y-s, z+s), (x+s, y+s, z+s), (x-s, y+s, z+s),  # top
    ]
    
    # Define edges as pairs of vertex indices
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # bottom face
        (4, 5), (5, 6), (6, 7), (7, 4),  # top face
        (0, 4), (1, 5), (2, 6), (3, 7),  # vertical edges
    ]
    
    x_coords, y_coords, z_coords = [], [], []
    for v1, v2 in edges:
        x_coords.extend([vertices[v1][0], vertices[v2][0], None])
        y_coords.extend([vertices[v1][1], vertices[v2][1], None])
        z_coords.extend([vertices[v1][2], vertices[v2][2], None])
    
    return x_coords, y_coords, z_coords


def create_cube_mesh(x, y, z, size=0.8):
    """
    Create a 3D solid cube mesh for visualization.
    """
    s = size / 2
    vertices = np.array([
        [x-s, y-s, z-s], [x+s, y-s, z-s], [x+s, y+s, z-s], [x-s, y+s, z-s],
        [x-s, y-s, z+s], [x+s, y-s, z+s], [x+s, y+s, z+s], [x-s, y+s, z+s],
    ])
    
    faces = np.array([
        [0, 1, 2], [0, 2, 3],  # bottom
        [4, 5, 6], [4, 6, 7],  # top
        [0, 1, 5], [0, 5, 4],  # front
        [2, 3, 7], [2, 7, 6],  # back
        [0, 3, 7], [0, 7, 4],  # left
        [1, 2, 6], [1, 6, 5],  # right
    ])
    
    return vertices, faces


def create_wall_between_cells(x1, y1, z1, x2, y2, z2, thickness=0.08):
    """
    Create a wall mesh between two adjacent cells.
    """
    # Calculate the midpoint
    mx, my, mz = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
    
    # Determine wall orientation
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    
    t = thickness / 2
    s = 0.45  # Half the cell size
    
    if dx != 0:  # Wall perpendicular to X axis
        vertices = np.array([
            [mx-t, my-s, mz-s], [mx+t, my-s, mz-s],
            [mx+t, my+s, mz-s], [mx-t, my+s, mz-s],
            [mx-t, my-s, mz+s], [mx+t, my-s, mz+s],
            [mx+t, my+s, mz+s], [mx-t, my+s, mz+s],
        ])
    elif dy != 0:  # Wall perpendicular to Y axis
        vertices = np.array([
            [mx-s, my-t, mz-s], [mx+s, my-t, mz-s],
            [mx+s, my+t, mz-s], [mx-s, my+t, mz-s],
            [mx-s, my-t, mz+s], [mx+s, my-t, mz+s],
            [mx+s, my+t, mz+s], [mx-s, my+t, mz+s],
        ])
    else:  # Wall perpendicular to Z axis
        vertices = np.array([
            [mx-s, my-s, mz-t], [mx+s, my-s, mz-t],
            [mx+s, my+s, mz-t], [mx-s, my+s, mz-t],
            [mx-s, my-s, mz+t], [mx+s, my-s, mz+t],
            [mx+s, my+s, mz+t], [mx-s, my+s, mz+t],
        ])
    
    faces = np.array([
        [0, 1, 2], [0, 2, 3],
        [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4],
        [2, 3, 7], [2, 7, 6],
        [0, 3, 7], [0, 7, 4],
        [1, 2, 6], [1, 6, 5],
    ])
    
    return vertices, faces


def create_maze_wireframe(engine):
    """
    Create wireframe visualization for the maze structure.
    Shows walls as lines forming corridors - making it look like a real maze.
    """
    all_x, all_y, all_z = [], [], []
    
    # Draw boundary walls
    w, h, d = engine.width, engine.height, engine.depth
    
    # Floor and ceiling grids
    for x in range(w + 1):
        # Bottom floor lines (front-back)
        all_x.extend([x, x, None])
        all_y.extend([0, 0, None])
        all_z.extend([0, d, None])
        # Top ceiling lines
        all_x.extend([x, x, None])
        all_y.extend([h, h, None])
        all_z.extend([0, d, None])
    
    for z in range(d + 1):
        # Bottom floor lines (left-right)
        all_x.extend([0, w, None])
        all_y.extend([0, 0, None])
        all_z.extend([z, z, None])
        # Top ceiling lines
        all_x.extend([0, w, None])
        all_y.extend([h, h, None])
        all_z.extend([z, z, None])
    
    # Vertical corner edges
    for x in [0, w]:
        for z in [0, d]:
            all_x.extend([x, x, None])
            all_y.extend([0, h, None])
            all_z.extend([z, z, None])
    
    # Draw internal walls based on maze structure
    for x in range(engine.width):
        for y in range(engine.height):
            for z in range(engine.depth):
                node = engine.grid[x][y][z]
                
                # Check for walls in each direction and draw them
                # East wall (between x and x+1)
                if node.walls.get('east', False) and x < engine.width - 1:
                    # Draw vertical line at x+0.5
                    all_x.extend([x + 1, x + 1, None])
                    all_y.extend([y, y + 1, None])
                    all_z.extend([z, z, None])
                    all_x.extend([x + 1, x + 1, None])
                    all_y.extend([y, y + 1, None])
                    all_z.extend([z + 1, z + 1, None])
                    all_x.extend([x + 1, x + 1, None])
                    all_y.extend([y, y, None])
                    all_z.extend([z, z + 1, None])
                    all_x.extend([x + 1, x + 1, None])
                    all_y.extend([y + 1, y + 1, None])
                    all_z.extend([z, z + 1, None])
                
                # North wall (between z and z+1)
                if node.walls.get('north', False) and z < engine.depth - 1:
                    all_x.extend([x, x, None])
                    all_y.extend([y, y + 1, None])
                    all_z.extend([z + 1, z + 1, None])
                    all_x.extend([x + 1, x + 1, None])
                    all_y.extend([y, y + 1, None])
                    all_z.extend([z + 1, z + 1, None])
                    all_x.extend([x, x + 1, None])
                    all_y.extend([y, y, None])
                    all_z.extend([z + 1, z + 1, None])
                    all_x.extend([x, x + 1, None])
                    all_y.extend([y + 1, y + 1, None])
                    all_z.extend([z + 1, z + 1, None])
                
                # Up wall (between y and y+1)
                if node.walls.get('up', False) and y < engine.height - 1:
                    all_x.extend([x, x + 1, None])
                    all_y.extend([y + 1, y + 1, None])
                    all_z.extend([z, z, None])
                    all_x.extend([x, x + 1, None])
                    all_y.extend([y + 1, y + 1, None])
                    all_z.extend([z + 1, z + 1, None])
                    all_x.extend([x, x, None])
                    all_y.extend([y + 1, y + 1, None])
                    all_z.extend([z, z + 1, None])
                    all_x.extend([x + 1, x + 1, None])
                    all_y.extend([y + 1, y + 1, None])
                    all_z.extend([z, z + 1, None])
    
    return all_x, all_y, all_z


def create_voxel_maze_visualization(engine, visited_nodes=None, final_path=None, 
                                    start=None, goal=None, title="3D Maze Pathfinding",
                                    show_walls=True, wall_opacity=0.3, wall_color='gray',
                                    animation_progress=1.0, show_path_animation=False):
    """
    Create an enhanced 3D maze visualization with wireframe walls and smooth animations.
    
    Args:
        engine: MazeEngine instance
        visited_nodes: List of (x,y,z) tuples for explored nodes
        final_path: List of (x,y,z) tuples for the solution path
        start: (x,y,z) tuple for start position
        goal: (x,y,z) tuple for goal position
        title: Plot title
        show_walls: Whether to render walls
        wall_opacity: Opacity of walls
        wall_color: Color of walls
        animation_progress: 0-1 value for path animation progress
        show_path_animation: Whether to animate the path line
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Create wireframe maze structure
    if show_walls:
        wx, wy, wz = create_maze_wireframe(engine)
        
        fig.add_trace(go.Scatter3d(
            x=wx, y=wy, z=wz,
            mode='lines',
            line=dict(color='rgba(100, 100, 120, 0.6)', width=2),
            name='Maze Walls',
            showlegend=True,
            hoverinfo='skip'
        ))
    
    # Draw visited nodes with gradient coloring based on visit order
    if visited_nodes and len(visited_nodes) > 0:
        vx, vy, vz = zip(*visited_nodes)
        # Create color gradient from light orange to deep orange based on visit order
        colors = [f'rgba(255, {max(100, 200 - i * 2)}, {max(50, 150 - i * 3)}, 0.7)' 
                  for i in range(len(visited_nodes))]
        
        fig.add_trace(go.Scatter3d(
            x=vx, y=vy, z=vz,
            mode='markers',
            marker=dict(
                size=4,
                color=list(range(len(visited_nodes))),
                colorscale='YlOrRd',
                opacity=0.6,
                showscale=False
            ),
            name='Explored Nodes',
            showlegend=True
        ))
    
    # Draw the path with animation effect
    if final_path and len(final_path) > 0:
        # Calculate how much of the path to show based on animation progress
        if show_path_animation:
            path_length = max(1, int(len(final_path) * animation_progress))
            animated_path = final_path[:path_length]
        else:
            animated_path = final_path
        
        px, py, pz = zip(*animated_path)
        
        # Draw the main path line with a glowing effect
        # Outer glow
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='lines',
            line=dict(color='rgba(0, 150, 255, 0.3)', width=12),
            name='Path Glow',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Main path line
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='lines+markers',
            line=dict(color='#00BFFF', width=6),
            marker=dict(size=4, color='#00BFFF', symbol='circle'),
            name='Solution Path',
            showlegend=True
        ))
        
        # Animated head of the path (current position)
        if show_path_animation and len(animated_path) > 0:
            head = animated_path[-1]
            fig.add_trace(go.Scatter3d(
                x=[head[0]], y=[head[1]], z=[head[2]],
                mode='markers',
                marker=dict(size=10, color='#FFD700', symbol='diamond',
                           line=dict(color='white', width=2)),
                name='Current Position',
                showlegend=True
            ))
    
    # Mark start position with a distinctive marker
    if start:
        fig.add_trace(go.Scatter3d(
            x=[start[0]], y=[start[1]], z=[start[2]],
            mode='markers',
            marker=dict(
                size=14, 
                color='#00FF7F',
                symbol='diamond',
                line=dict(color='#006400', width=3)
            ),
            name='Start',
            showlegend=True
        ))
    
    # Mark goal position with a distinctive marker
    if goal:
        fig.add_trace(go.Scatter3d(
            x=[goal[0]], y=[goal[1]], z=[goal[2]],
            mode='markers',
            marker=dict(
                size=14, 
                color='#FF4500',
                symbol='diamond',
                line=dict(color='#8B0000', width=3)
            ),
            name='Goal',
            showlegend=True
        ))
    
    # Configure layout with dark theme matching the app
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#e0e0e0', family='Arial Black')
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text='X', font=dict(color='#a0a0a0')),
                tickfont=dict(color='#808080'),
                backgroundcolor="rgb(22, 33, 62)",
                gridcolor="rgba(100, 130, 180, 0.2)",
                showbackground=True,
                range=[-0.5, engine.width + 0.5],
                showgrid=True,
                zeroline=False
            ),
            yaxis=dict(
                title=dict(text='Y (Height)', font=dict(color='#a0a0a0')),
                tickfont=dict(color='#808080'),
                backgroundcolor="rgb(22, 33, 62)",
                gridcolor="rgba(100, 130, 180, 0.2)",
                showbackground=True,
                range=[-0.5, engine.height + 0.5],
                showgrid=True,
                zeroline=False
            ),
            zaxis=dict(
                title=dict(text='Z', font=dict(color='#a0a0a0')),
                tickfont=dict(color='#808080'),
                backgroundcolor="rgb(22, 33, 62)",
                gridcolor="rgba(100, 130, 180, 0.2)",
                showbackground=True,
                range=[-0.5, engine.depth + 0.5],
                showgrid=True,
                zeroline=False
            ),
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.5),
                up=dict(x=0, y=1, z=0)
            )
        ),
        paper_bgcolor='rgba(26, 26, 46, 0.95)',
        plot_bgcolor='rgba(22, 33, 62, 0.95)',
        height=700,
        margin=dict(l=0, r=0, t=60, b=0),
        legend=dict(
            x=0.02, y=0.98,
            bgcolor='rgba(26, 26, 46, 0.9)',
            bordercolor='rgba(100, 126, 234, 0.5)',
            borderwidth=1,
            font=dict(size=11, color='#e0e0e0')
        )
    )
    
    return fig


def create_simple_voxel_maze(engine, show_path_cells=False, path=None):
    """
    Create a simplified voxel visualization showing only the maze structure.
    """
    fig = go.Figure()
    path_set = set(path) if path else set()
    
    # Create wireframe for the maze
    wx, wy, wz = create_maze_wireframe(engine)
    fig.add_trace(go.Scatter3d(
        x=wx, y=wy, z=wz,
        mode='lines',
        line=dict(color='rgba(100, 100, 120, 0.5)', width=1.5),
        name='Maze Structure',
        showlegend=True
    ))
    
    # Highlight path cells if provided
    if path and show_path_cells:
        px, py, pz = zip(*path)
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='lines+markers',
            line=dict(color='blue', width=5),
            marker=dict(size=4, color='blue'),
            name='Path',
            showlegend=True
        ))
    
    fig.update_layout(
        title="Maze Structure",
        scene=dict(
            xaxis=dict(title='X', backgroundcolor="rgb(200, 200, 230)"),
            yaxis=dict(title='Y', backgroundcolor="rgb(200, 200, 230)"),
            zaxis=dict(title='Z', backgroundcolor="rgb(200, 200, 230)"),
            aspectmode='cube'
        ),
        height=700
    )
    
    return fig