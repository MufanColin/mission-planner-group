import numpy as np
import matplotlib.pyplot as plt

from multi_ant_colony import MultiAntColony  # Ensure this imports your AntColony class
from galogic import *  # Assuming Dustbin and RouteManager are defined here
from globals import *


if __name__ == "__main__":
    # Assuming numNodes and seedValue are defined
    np.random.seed(seedValue)
    random.seed(seedValue)

    # Add Dustbins
    for i in range(numNodes):
        RouteManager.addDustbin(Dustbin())

    # Create distance matrix
    distance_matrix = np.zeros((numNodes, numNodes))
    for i in range(numNodes):
        for j in range(numNodes):
            if i == j:
                distance_matrix[i][j] = np.inf  # Ants don't stay in one place
            else:
                distance_matrix[i][j] = RouteManager.getDustbin(i).distanceTo(
                    RouteManager.getDustbin(j)
                )

    # Ant Colony Optimization parameters
    config = dict(
        n_ants=numTrucks,
        n_best=10,
        n_iterations=1000,
        decay=0.95,
        n_accumulate=10,
        alpha=1,
        beta=2,
        p0=0.5,
    )

    # Initialize Ant Colony
    ant_colony = MultiAntColony(distance_matrix, **config)
    # Run ACO with progress bar
    shortest_pathset, record = ant_colony.run()
    xaxis, yaxis = [i[0] for i in record], [i[1] for i in record]

    print("Global minimum distance:", shortest_pathset[1])
    print(
        "Final Path Seq len:",
        [len(shortest_pathset[0][i]) for i in range(len(shortest_pathset[0]))],
    )
    print("Final path idx", shortest_pathset[0])
    final_paths = [
        "|".join(
            [RouteManager.getDustbin(i[0]).toString() for i in path]
            + [RouteManager.getDustbin(path[-1][1]).toString()]
        )
        for path in shortest_pathset[0]
    ]
    final_paths = "\n".join([f"path{i}:{path}" for i, path in enumerate(final_paths)])
    print("Final Path:", final_paths)
    check_set = set()
    for path in shortest_pathset[0]:
        for p in path:
            check_set.add(p[0])
            check_set.add(p[1])
    assert len(check_set) == numNodes
    assert len(shortest_pathset[0]) == numTrucks
    # Plot the results
    fig = plt.figure()
    plt.plot(xaxis, yaxis, "r-")
    plt.xlabel("Iterations")
    plt.ylabel("Shortest Path Distance")
    plt.title("Ant Colony Optimization")
    fig.savefig(f"multiantcolony_nodes-{numNodes}_drones-{numTrucks}.png")
    with open(f"multiantcolony_nodes-{numNodes}_drones-{numTrucks}.txt", "w") as f:
        print(f"Global minimum distance: {shortest_pathset[1]}", file=f)
        print(
            "Final Path Seq len:",
            [len(shortest_pathset[0][i]) for i in range(len(shortest_pathset[0]))],
            file=f,
        )
        print("Final Path:", final_paths)

    plt.show()
