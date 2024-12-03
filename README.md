# Genetic Algorithm to solve Multiple Traveling Salesman Problem
Here graph is covered using different agents having different routes.

Routes only intersect at initial node.

main.py 作为 Baseline.

共有`numTrucks`个无人机（truck），`numNodes`个检查点(dustbin)
第1个dustbin(index=0)是基地。

## `Route`类
`Route`类维护`numTrucks`个无人机的路线集合。

`Route.length`: `numTrucks`个无人机的路线的长度（包含的检查点的数量），是一个长度为`numTrucks`的列表。

`Route.route`: `numTrucks`个无人机的路线，包含`numTrucks`个列表。`route[i]`是长度为`length[i]`的`Dustbin`类的列表，第一个元素都是`dustbin[0]`。

## `Population`类
`Population`类维护大小为`populationSize`的种群，内含`populationSize`个`Route`类的无人机路线集合。

## `GA`类
执行遗传算法。

`elitism`精英主义，上代种群中的最优者会被保留下来。

`tournamentSelection`：选择操作，从上一代种群中随机选择`tournamentSize`个个体，从中选择最优的个体（总路线长度最短）返回。

`crossover`：交叉操作，对选择的两个个体交叉，生成下一代个体。

`mutate`: 变异操作。