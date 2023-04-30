import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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

# Define the edges of the graph based on adjacent hexagons
edges = [
    ((0,1), (1,0)), ((0,1), (0,2)), ((0,1), (1,2)), ((0,1), (1,1)), ((0,2), (0,3)), ((0,2), (1,2)), ((0,3), (1,3)), ((0,3), (1,2)), ((0,3), (1,4)),
    ((1,0), (2,0)), ((1,0), (1,1)), ((1,0), (1,1)), ((1,1), (1,2)), ((1,4), (2,4)), ((1,4), (1,3)), ((1,1),(2,1)), ((1,2),(1,3)), ((1,3),(2,2)), ((1,1),(2,2)), ((2,3), (3,2)),
    ((2,0), (3,0)), ((2,0), (2,1)), ((2,1), (2,2)), ((2,2), (2,3)), ((2,4), (3,4)), ((2,4), (1,3)), ((2,4), (2,3)), ((2,3), (3,3)), ((3,1), (2,1)), ((3,2), (2,1)), ((2,2), (3,2)),
    ((3,0), (3,1)), ((3,0), (2,1)), ((3,1), (3,2)), ((3,2), (3,3)), ((3,3), (3,4)), ((3,2), (3,3)), ((3,4), (2,3)), ((3,3),(4,2)), ((3,1), (4,2)),
    ((1,1), (2,0)), ((1,1), (2,1)), ((1,2), (2,2)), ((1,3), (2,3)), ((3,2),(4,2))
    ]

# Create a graph object using NetworkX
G = nx.Graph()

# Add the nodes to the graph object
G.add_nodes_from(board.keys())

# Add the edges to the graph object
G.add_edges_from(edges)

# Define terrain colors
terrain_colors = {
    "forest": "#008000",
    "pasture": "#00ff00",
    "field": "#ffff00",
    "hill": "#8b4513",
    "mountain": "#d3d3d3",
    "desert": "#ffa500"
}

# Define the positions of the nodes based on the coordinates of the hexagons
node_positions = {}
node_colors = []
for (i, j), terrain in board.items():
    x = ((i - 2) * np.sqrt(3) + (j % 2) * np.sqrt(3) / 2)/2
    y = (j - 2) * 1.5/2
    node_positions[(i, j)] = (x, y)
    node_colors.append(terrain_colors[terrain])

# Draw the graph using the node positions and edge connections
fig, ax = plt.subplots()
nx.draw_networkx_nodes(G, pos=node_positions, node_size=100, node_color=node_colors, edgecolors='black', ax=ax)
nx.draw_networkx_edges(G, pos=node_positions, ax=ax)
ax.axis('equal')
ax.set_xlim(-2 * np.sqrt(3) - 0.5, 2 * np.sqrt(3) + 0.5)
ax.set_ylim(-4.5, 4.5)
ax.axis('off')
plt.show()

