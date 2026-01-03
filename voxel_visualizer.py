"""
Voxel-style 3D visualization for maze walls.
Renders walls as actual 3D blocks/cubes using Plotly Mesh3d.
"""

import plotly.graph_objects as go
import numpy as np


def create_cube_mesh(x, y, z, size=0.5, color='gray', opacity=0.3):
    """
    Create a 3D cube mesh for a voxel.
    
    Args:
        x, y, z: Center position of the cube
        size: Size of the cube (default 0.5 for spacing)
        color: Color of the cube
        opacity: Opacity of the cube
    
    Returns:
        vertices, faces, colors for Mesh3d
    """
    # Define the 8 vertices of a cube
    s = size / 2
    vertices = np.array([
        [x-s, y-s, z-s],  # 0: bottom-left-back
        [x+s, y-s, z-s],  # 1: bottom-right-back
        [x+s, y+s, z-s],  # 2: bottom-right-front
        [x-s, y+s, z-s],  # 3: bottom-left-front
        [x-s, y-s, z+s],  # 4: top-left-back
        [x+s, y-s, z+s],  # 5: top-right-back
        [x+s, y+s, z+s],  # 6: top-right-front
        [x-s, y+s, z+s],  # 7: top-left-front
    ])
    
    # Define the 12 triangular faces (2 per cube face)
    faces = np.array([
        [0, 1, 2], [0, 2, 3],  # bottom
        [4, 5, 6], [4, 6, 7],  # top
        [0, 1, 5], [0, 5, 4],  # back
        [2, 3, 7], [2, 7, 6],  # front
        [0, 3, 7], [0, 7, 4],  # left
        [1, 2, 6], [1, 6, 5],  # right
    ])
    
    return vertices, faces


def create_wall_voxel(x, y, z, direction, thickness=0.1, length=0.9):
    """
    Create a wall voxel between two cells.
    
    Args:
        x, y, z: Cell position
        direction: Wall direction ('east', 'west', 'north', 'south', 'up', 'down')
        thickness: Thickness of the wall
        length: Length of the wall along the cell edge
    
    Returns:
        vertices, faces for the wall mesh
    """
    # Wall positions based on direction
    t = thickness / 2
    l = length / 2
    
    if direction == 'east':  # Wall on +X side
        vertices = np.array([
            [x+0.5-t, y-l, z-l], [x+0.5+t, y-l, z-l],
            [x+0.5+t, y+l, z-l], [x+0.5-t, y+l, z-l],
            [x+0.5-t, y-l, z+l], [x+0.5+t, y-l, z+l],
            [x+0.5+t, y+l, z+l], [x+0.5-t, y+l, z+l],
        ])
    elif direction == 'west':  # Wall on -X side
        vertices = np.array([
            [x-0.5-t, y-l, z-l], [x-0.5+t, y-l, z-l],
            [x-0.5+t, y+l, z-l], [x-0.5-t, y+l, z-l],
            [x-0.5-t, y-l, z+l], [x-0.5+t, y-l, z+l],
            [x-0.5+t, y+l, z+l], [x-0.5-t, y+l, z+l],
        ])
    elif direction == 'north':  # Wall on +Z side
        vertices = np.array([
            [x-l, y-l, z+0.5-t], [x+l, y-l, z+0.5-t],
            [x+l, y+l, z+0.5-t], [x-l, y+l, z+0.5-t],
            [x-l, y-l, z+0.5+t], [x+l, y-l, z+0.5+t],
            [x+l, y+l, z+0.5+t], [x-l, y+l, z+0.5+t],
        ])
    elif direction == 'south':  # Wall on -Z side
        vertices = np.array([
            [x-l, y-l, z-0.5-t], [x+l, y-l, z-0.5-t],
            [x+l, y+l, z-0.5-t], [x-l, y+l, z-0.5-t],
            [x-l, y-l, z-0.5+t], [x+l, y-l, z-0.5+t],
            [x+l, y+l, z-0.5+t], [x-l, y+l, z-0.5+t],
        ])
    elif direction == 'up':  # Wall on +Y side
        vertices = np.array([
            [x-l, y+0.5-t, z-l], [x+l, y+0.5-t, z-l],
            [x+l, y+0.5-t, z+l], [x-l, y+0.5-t, z+l],
            [x-l, y+0.5+t, z-l], [x+l, y+0.5+t, z-l],
            [x+l, y+0.5+t, z+l], [x-l, y+0.5+t, z+l],
        ])
    else:  # 'down' - Wall on -Y side
        vertices = np.array([
            [x-l, y-0.5-t, z-l], [x+l, y-0.5-t, z-l],
            [x+l, y-0.5-t, z+l], [x-l, y-0.5-t, z+l],
            [x-l, y-0.5+t, z-l], [x+l, y-0.5+t, z-l],
            [x+l, y-0.5+t, z+l], [x-l, y-0.5+t, z+l],
        ])
    
    # Define triangular faces
    faces = np.array([
        [0, 1, 2], [0, 2, 3],  # bottom
        [4, 5, 6], [4, 6, 7],  # top
        [0, 1, 5], [0, 5, 4],  # back
        [2, 3, 7], [2, 7, 6],  # front
        [0, 3, 7], [0, 7, 4],  # left
        [1, 2, 6], [1, 6, 5],  # right
    ])
    
    return vertices, faces


def create_voxel_maze_visualization(engine, visited_nodes=None, final_path=None, 
                                    start=None, goal=None, title="3D Voxel Maze",
                                    show_walls=True, wall_opacity=0.2, wall_color='gray'):
    """
    Create a voxel-style 3D maze visualization with thick walls.
    
    Args:
        engine: MazeEngine instance
        visited_nodes: List of (x,y,z) tuples for explored nodes
        final_path: List of (x,y,z) tuples for the solution path
        start: (x,y,z) tuple for start position
        goal: (x,y,z) tuple for goal position
        title: Plot title
        show_walls: Whether to render wall voxels
        wall_opacity: Opacity of wall voxels (0-1)
        wall_color: Color of wall voxels
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Collect all wall meshes
    if show_walls:
        all_vertices = []
        all_faces = []
        vertex_offset = 0
        
        # Iterate through all cells and render their walls
        for x in range(engine.width):
            for y in range(engine.height):
                for z in range(engine.depth):
                    node = engine.grid[x][y][z]
                    
                    # Check each direction for walls
                    for direction, has_wall in node.walls.items():
                        if has_wall:
                            # Only render walls on the positive directions to avoid duplicates
                            # or render boundary walls
                            should_render = False
                            
                            if direction == 'east' and (x == engine.width - 1 or 
                                                        engine.grid[x+1][y][z].walls['west']):
                                should_render = True
                            elif direction == 'north' and (z == engine.depth - 1 or
                                                          engine.grid[x][y][z+1].walls['south']):
                                should_render = True
                            elif direction == 'up' and (y == engine.height - 1 or
                                                       engine.grid[x][y+1][z].walls['down']):
                                should_render = True
                            elif direction == 'west' and x == 0:
                                should_render = True
                            elif direction == 'south' and z == 0:
                                should_render = True
                            elif direction == 'down' and y == 0:
                                should_render = True
                            
                            if should_render:
                                vertices, faces = create_wall_voxel(x, y, z, direction)
                                
                                # Adjust face indices for the combined mesh
                                adjusted_faces = faces + vertex_offset
                                
                                all_vertices.append(vertices)
                                all_faces.append(adjusted_faces)
                                vertex_offset += len(vertices)
        
        # Combine all wall meshes
        if all_vertices:
            combined_vertices = np.vstack(all_vertices)
            combined_faces = np.vstack(all_faces)
            
            # Add the combined mesh to the plot
            fig.add_trace(go.Mesh3d(
                x=combined_vertices[:, 0],
                y=combined_vertices[:, 1],
                z=combined_vertices[:, 2],
                i=combined_faces[:, 0],
                j=combined_faces[:, 1],
                k=combined_faces[:, 2],
                color=wall_color,
                opacity=wall_opacity,
                name='Walls',
                showlegend=True,
                hoverinfo='skip'
            ))
    
    # Draw visited nodes as small spheres
    if visited_nodes:
        vx, vy, vz = zip(*visited_nodes)
        fig.add_trace(go.Scatter3d(
            x=vx, y=vy, z=vz,
            mode='markers',
            marker=dict(size=3, color='orange', opacity=0.6),
            name='Explored',
            showlegend=True
        ))
    
    # Draw final path as a thick line with markers
    if final_path:
        px, py, pz = zip(*final_path)
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='lines+markers',
            line=dict(color='blue', width=8),
            marker=dict(size=5, color='blue', symbol='circle'),
            name='Path',
            showlegend=True
        ))
    
    # Mark start position
    if start:
        fig.add_trace(go.Scatter3d(
            x=[start[0]], y=[start[1]], z=[start[2]],
            mode='markers',
            marker=dict(size=12, color='green', symbol='diamond',
                       line=dict(color='darkgreen', width=2)),
            name='Start',
            showlegend=True
        ))
    
    # Mark goal position
    if goal:
        fig.add_trace(go.Scatter3d(
            x=[goal[0]], y=[goal[1]], z=[goal[2]],
            mode='markers',
            marker=dict(size=12, color='red', symbol='diamond',
                       line=dict(color='darkred', width=2)),
            name='Goal',
            showlegend=True
        ))
    
    # Configure layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#333', family='Arial Black')
        ),
        scene=dict(
            xaxis=dict(
                title='X',
                backgroundcolor="rgb(240, 240, 240)",
                gridcolor="white",
                showbackground=True,
                range=[-0.5, engine.width - 0.5]
            ),
            yaxis=dict(
                title='Y',
                backgroundcolor="rgb(240, 240, 240)",
                gridcolor="white",
                showbackground=True,
                range=[-0.5, engine.height - 0.5]
            ),
            zaxis=dict(
                title='Z',
                backgroundcolor="rgb(240, 240, 240)",
                gridcolor="white",
                showbackground=True,
                range=[-0.5, engine.depth - 0.5]
            ),
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        height=700,
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(
            x=0.02, y=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='gray',
            borderwidth=1
        )
    )
    
    return fig


def create_simple_voxel_maze(engine, show_path_cells=False, path=None):
    """
    Create a simplified voxel visualization showing only the maze structure.
    
    Args:
        engine: MazeEngine instance
        show_path_cells: If True, highlight path cells
        path: List of (x,y,z) tuples for the path
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Create cells as cubes
    path_set = set(path) if path else set()
    
    for x in range(engine.width):
        for y in range(engine.height):
            for z in range(engine.depth):
                node = engine.grid[x][y][z]
                
                # Determine cell color
                if (x, y, z) in path_set:
                    color = 'blue'
                    opacity = 0.7
                    show = True
                elif not node.is_wall:
                    color = 'lightgray'
                    opacity = 0.1
                    show = False  # Don't show empty cells by default
                else:
                    color = 'gray'
                    opacity = 0.4
                    show = True
                
                if show or show_path_cells:
                    vertices, faces = create_cube_mesh(x, y, z, size=0.9, 
                                                       color=color, opacity=opacity)
                    
                    fig.add_trace(go.Mesh3d(
                        x=vertices[:, 0],
                        y=vertices[:, 1],
                        z=vertices[:, 2],
                        i=faces[:, 0],
                        j=faces[:, 1],
                        k=faces[:, 2],
                        color=color,
                        opacity=opacity,
                        showlegend=False,
                        hoverinfo='skip'
                    ))
    
    # Configure layout
    fig.update_layout(
        title="Voxel Maze Structure",
        scene=dict(
            xaxis=dict(title='X', backgroundcolor="rgb(200, 200, 230)"),
            yaxis=dict(title='Y', backgroundcolor="rgb(200, 200, 230)"),
            zaxis=dict(title='Z', backgroundcolor="rgb(200, 200, 230)"),
            aspectmode='cube'
        ),
        height=700
    )
    
    return fig