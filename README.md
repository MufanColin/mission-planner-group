# Genetic Algorithm to solve Multiple Traveling Salesman Problem
Here graph is covered using different agents having different routes.

Routes only intersect at initial node.

main.py 作为 Baseline.

共有`numTrucks`个无人机（truck），`numNodes`个检查点(dustbin)
第1个dustbin(index=0)是基地。

`Route`类维护`numTrucks`个无人机的路线集合。

`Route.length`: `numTrucks`个无人机的路线的长度（包含的检查点的数量），是一个长度为`numTrucks`的列表。

`Route.route`: `numTrucks`个无人机的路线，包含`numTrucks`个列表。`route[i]`是长度为`length[i]`的`Dustbin`类的列表，第一个元素都是`dustbin[0]`