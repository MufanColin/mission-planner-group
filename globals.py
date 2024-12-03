import random
import math
'''
Contains all global variables specific to simulation
'''
# Defines range for coordinates when dustbins are randomly scattered
xMax = 1000
yMax = 1000
seedValue = 1
numNodes = 500 # 检查点数量
numGenerations = 70
# size of population
populationSize = 100 
mutationRate = 0.02
tournamentSize = 10
elitism = True
# number of trucks
numTrucks = 30# 无人机数量

def random_range(n, total, ub, lb):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    # dividers = sorted(random.sample(range(1, total), n - 1))
    # return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
    while True:
        r = [ random.randint(int(lb), int(ub)+1) for _ in range(n)]
        r = [round(i/sum(r)*total) for i in r]
        r_sum = sum(r)
        t = random.randint(0, n-1)
        if total-r_sum+r[t]>0:
            r[t] = total-r_sum+r[t]
            # for i in r:
            #     assert isinstance(i, int), f"{r}"
            return r
            

# Randomly distribute number of dustbins to subroutes
# Maximum and minimum values are maintained to reach optimal result
def route_lengths():

    '''
    return:list[int] numTrucks integers(rout_legth) suming to upper
    '''
    upper = (numNodes + numTrucks - 1)
    fa = upper/numTrucks*1.2 # max route length
    fb = upper/numTrucks*0.8 # min route length
    a = random_range(numTrucks, upper, fa, fb)
    # while 1:
    #     if all( i < fa and i > fb  for i in a):
    #         break
    #     else:
    #         a = random_range(numTrucks, upper)
    return a
