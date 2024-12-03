import numpy as np
import matplotlib.pyplot as plt
import progressbar
from ant_colony import AntColony  # Ensure this imports your AntColony class
from galogic import *  # Assuming Dustbin and RouteManager are defined here

# Assuming numNodes and seedValue are defined
np.random.seed(seedValue)
random.seed(seedValue)

numNodes = 200

def path_edges_to_nodes(path_edges):
    path_nodes = [path_edges[0][0]]
    for edge in path_edges:
        path_nodes.append(edge[1])
    return path_nodes

# Add Dustbins with x and y coordinates
for i in range(numNodes):
    x = np.random.rand()  # Replace with actual x coordinate generation
    y = np.random.rand()  # Replace with actual y coordinate generation
    RouteManager.addDustbin(Dustbin(x, y))  # Ensure Dustbin class accepts coordinates

# Collect dustbin coordinates
dustbin_x = [RouteManager.getDustbin(i).x for i in range(numNodes)]
dustbin_y = [RouteManager.getDustbin(i).y for i in range(numNodes)]

# Create distance matrix
num_dustbins = numNodes
distance_matrix = np.zeros((num_dustbins, num_dustbins))
for i in range(num_dustbins):
    for j in range(num_dustbins):
        if i == j:
            distance_matrix[i][j] = np.inf  # Ants don't stay in one place
        else:
            distance_matrix[i][j] = RouteManager.getDustbin(i).distanceTo(RouteManager.getDustbin(j))

# Ant Colony Optimization parameters
n_ants = 20
n_best = 10
n_iterations = 10
decay = 0.95
alpha = 1
beta = 2

# Initialize Ant Colony
ant_colony = AntColony(distance_matrix, n_ants, n_best, n_iterations, decay, alpha, beta)

# Run ACO
all_time_shortest_path, all_ant_paths = ant_colony.run()

# Convert all ants' paths from edges to nodes
all_ant_node_paths = [path_edges_to_nodes(path) for path in all_ant_paths]

# Plot all ant trajectories
fig, ax = plt.subplots(figsize=(10, 10))
# Plot dustbin positions
ax.scatter(dustbin_x, dustbin_y, s=5, c='gray', label='Dustbins')

# Plot each ant's path
for path_nodes in all_ant_node_paths:
    path_x = [dustbin_x[node] for node in path_nodes]
    path_y = [dustbin_y[node] for node in path_nodes]
    ax.plot(path_x, path_y, 'b-', alpha=0.1)  # Adjust alpha for better visualization

# Plot the shortest path
shortest_path_nodes = path_edges_to_nodes(all_time_shortest_path[0])
shortest_path_x = [dustbin_x[node] for node in shortest_path_nodes]
shortest_path_y = [dustbin_y[node] for node in shortest_path_nodes]
ax.plot(shortest_path_x, shortest_path_y, 'r-', linewidth=2, label='Shortest Path')

ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_title('Ant Colony Optimization - All Ant Trajectories')
ax.legend()
plt.show()