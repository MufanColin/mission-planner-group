import numpy as np
import matplotlib.pyplot as plt
import progressbar
from ant_colony import AntColony  # Ensure this imports your AntColony class
from galogic import *  # Assuming Dustbin and RouteManager are defined here

# Assuming numNodes and seedValue are defined
np.random.seed(seedValue)
random.seed(seedValue)

numNodes = 500

# Add Dustbins
for i in range(numNodes):
    RouteManager.addDustbin(Dustbin())

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
n_ants = 30
n_best = 10
n_iterations = 10
decay = 0.95
alpha = 1
beta = 2

# Initialize Ant Colony
ant_colony = AntColony(distance_matrix, n_ants, n_best, n_iterations, decay, alpha, beta)

# Lists to track progress
yaxis = []  # Shortest distance in each iteration
xaxis = []  # Iteration count

# Run ACO with progress bar
pbar = progressbar.ProgressBar(maxval=n_iterations)
shortest_path = ("placeholder", np.inf)
for i in pbar(range(n_iterations)):
    current_shortest = ant_colony.run()
    if current_shortest[1] < shortest_path[1]:
        shortest_path = current_shortest
    yaxis.append(shortest_path[1])
    xaxis.append(i)

print('Global minimum distance:', shortest_path[1])
print('Final Path:', shortest_path[0])

# Plot the results
fig = plt.figure()
plt.plot(xaxis, yaxis, 'r-')
plt.xlabel('Iterations')
plt.ylabel('Shortest Path Distance')
plt.title('Ant Colony Optimization')
fig.savefig(f'antcolony_nodes-{numNodes}_drones-{numTrucks}.png')
plt.show()