import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.transforms import Affine2D

def generate_game_board():
    hexagons = [
        (0, 1), (0, 2), (0, 3), 
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4,2) 
    ]

    terrain_counts = {
        "forest": 4,
        "pasture": 4,
        "field": 4,
        "hill": 3,
        "mountain": 3,
        "desert": 1
    }

    terrain_types = []
    for terrain, count in terrain_counts.items():
        terrain_types.extend([terrain] * count)

    np.random.shuffle(terrain_types)

    board = {}
    for i, position in enumerate(hexagons):
        board[position] = terrain_types[i]

    return board

board = generate_game_board()

terrain_colors = {
    "forest": "#008000",
    "pasture": "#00ff00",
    "field": "#ffff00",
    "hill": "#8b4513",
    "mountain": "#d3d3d3",
    "desert": "#ffa500"
}

border_color = "black"

fig, ax = plt.subplots()

# Add an outer hexagon to the plot
outer_polygon = RegularPolygon((0, 0), 6, 2.75, edgecolor='none', facecolor='#87CEEB')
outer_transform = Affine2D().rotate_deg(30)
outer_polygon.set_transform(outer_transform + ax.transData)
ax.add_patch(outer_polygon)
outer_polygon.set_linewidth(1)
outer_polygon.set_edgecolor('black')

# Get the vertices of the outer hexagon
center = (0, 0)
radius = 2.75
angles = np.linspace(0, 2*np.pi, 7)[:-1]
outer_vertices = [(center[0] + radius*np.cos(a), center[1] + radius*np.sin(a)) for a in angles]

# Define inner vertices
inner_radius = (2.75+0.5*2)/(np.sqrt(3))
inner_angles = np.linspace(0, 2*np.pi, 7)[:-1]
inner_vertices = [(center[0] + inner_radius*np.cos(a), center[1] + inner_radius*np.sin(a)) for a in inner_angles]

# Connect the inner and outer vertices with lines
for i in range(6):
    ax.plot([outer_vertices[i][0], inner_vertices[i][0]], [outer_vertices[i][1], inner_vertices[i][1]], color='black',linewidth=1)

x_coords = {}
y_coords = {}
polygons = []

for (i, j), terrain in board.items():
    x = ((i - 2) * np.sqrt(3) + (j % 2) * np.sqrt(3) / 2)/2
    y = (j - 2) * 1.5/2
    x_coords[(i, j)] = x
    y_coords[(i, j)] = y

    polygon = RegularPolygon((x, y), 6, 0.5, edgecolor=border_color, facecolor=terrain_colors[terrain])
    polygons.append(polygon)

for polygon in polygons:
    ax.add_patch(polygon)

ax.axis('equal')
ax.set_xlim(-2 * np.sqrt(3) - 0.5, 2 * np.sqrt(3) + 0.5)
ax.set_ylim(-4.5, 4.5)
ax.axis('off')

# Create a legend for the terrain colors
legend_elements = []
for terrain, color in terrain_colors.items():
    patch = plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor='none')
    legend_elements.append((patch, terrain))

ax.legend(*zip(*legend_elements), loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)

plt.show()