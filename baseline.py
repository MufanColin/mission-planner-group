import matplotlib.pyplot as plt
import progressbar
from galogic import *

random.seed(seedValue)
pbar = progressbar.ProgressBar(maxval=numGenerations)

# Add Dustbins
for i in range(numNodes):
    RouteManager.addDustbin(Dustbin())

yaxis = []  # Fittest value (distance)
xaxis = []  # Generation count

pop = Population(populationSize, True)
globalRoute = pop.getFittest()
print("Initial minimum distance: " + str(globalRoute.getDistance()))

# Start evolving

for i in pbar(range(numGenerations)):
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)

print("Global minimum distance: " + str(globalRoute.getDistance()))
print("Final Route: " + globalRoute.toString())

fig = plt.figure()

plt.plot(xaxis, yaxis, "r-")
plt.xlabel("Iterations")
plt.ylabel("Shortest Path Distance")
plt.title("Baseline")
fig.savefig(f"baseline_nodes-{numNodes}_drones-{numTrucks}.png")
with open(f"baseline_nodes-{numNodes}_drones-{numTrucks}.txt", "w") as f:
    print("Global minimum distance: " + str(globalRoute.getDistance()), file=f)
    print("Final Route: " + globalRoute.toString(), file=f)
plt.show()
