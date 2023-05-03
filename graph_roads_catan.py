import networkx as nx
import numpy as np
import matplotlib.pylab as plt

import numpy as np

def generate_board_vertices():
    hexagons = [
        (0, 1), (0, 2), (0, 3), 
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 2) 
    ]
    
    vertices = []
    
    for position in hexagons:
        i, j = position
        x_center = ((i - 2) * np.sqrt(3) + (j % 2) * np.sqrt(3) / 2)/2
        y_center = (j - 2) * 1.5/2
        side_length = 0.5

        # Calculate the vertex positions with a 30 degree rotation
        angle_offset = np.pi/6
        vertex_coords = [
            (x_center + side_length * np.cos(angle + angle_offset), y_center + side_length * np.sin(angle + angle_offset))
            for angle in np.linspace(0, 2*np.pi, 7)[:-1]
        ]
        vertices.append(vertex_coords)
    
    return vertices

vertices = generate_board_vertices()

import networkx as nx
from scipy.spatial.distance import pdist, squareform

vertices = generate_board_vertices()

# Compute the pairwise distances between vertices
distances = squareform(pdist(np.vstack(vertices)))

# Create a graph
G = nx.Graph()

# Add nodes to the graph
for i, vertex_list in enumerate(vertices):
    for j, vertex in enumerate(vertex_list):
        G.add_node((i,j), pos=vertex)

# Add edges between adjacent hexagons
for i in range(len(vertices)):
    for j in range(len(vertices[i])):
        neighbors = [(i-1,j-1), (i-1,j), (i,j-1), (i,j+1), (i+1,j), (i+1,j+1)]
        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor[0] < len(vertices) and neighbor[1] >= 0 and neighbor[1] < len(vertices[0]):
                distance = np.linalg.norm(np.array(vertices[i][j]) - np.array(vertices[neighbor[0]][neighbor[1]]))
                if abs(distance - 0.5) < 1e-10:
                    G.add_edge((i,j), neighbor)

# Manually add the missing edges on the right side
missing_edges = []
missing_edges.append(((18, 0), (18, 5)))
missing_edges.append(((18, 4), (14, 5)))
missing_edges.append(((13, 5), (14, 4)))
missing_edges.append(((16, 0), (16, 5)))
missing_edges.append(((17, 0), (17, 5)))

for edge in missing_edges:
    G.add_edge(*edge)

# Draw the graph
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos=pos, with_labels=False, node_size=10)
plt.axis("equal")
plt.show()

