import random as rn
import numpy as np
import progressbar
import time
import multiprocessing

class MultiAntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, n_accumulate, decay, alpha=1, beta=1, p0=0.1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances# （n_nodes, n_nodes）
        self.n_nodes = len(distances)
        self.pheromone = np.ones(self.distances.shape) / len(distances)# (n_nodes, n_nodes)
        self.all_inds =  np.arange(0, len(distances), 1)#(n_nodes,) 
        self.n_best = n_best# n_best ants spread pheromone
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay# pheromone decay
        self.n_accumulate = n_accumulate
        self.alpha = alpha
        self.beta = beta
        self.p0 = p0

    def run(self):
        '''
        Returns:
            global_shortest_pathset (tuple): (path_set, path_set_len)

            shortest_pathset_record (list): list[(iter_idx, path_len)]
            
        '''
        global_shortest_pathset = ("placeholder", np.inf)
        shortest_pathset_record = []
        pbar = progressbar.ProgressBar(maxval=self.n_iterations)(range(self.n_iterations))
        for i in pbar:
            pathset_l = []
            # pool = multiprocessing.Pool()
            # pathset_l = pool.starmap(self.gen_pathset, [() for _ in range(self.n_accumulate)])
            # pathset_l = [pool.apply(self.gen_pathset ) for _ in range(self.n_accumulate) ]
            # pathset_l = pool.map(self.gen_pathset, [None for _ in range(self.n_accumulate)])
            for j in range(self.n_accumulate):
                pathset_l.append(self.gen_pathset())
            self.spread_pheronome(pathset_l)
            shortest_pathset = min(pathset_l, key=lambda x: x[1])
            if shortest_pathset[1] < global_shortest_pathset[1]:
                global_shortest_pathset = shortest_pathset       
            shortest_pathset_record.append((i, global_shortest_pathset[1]))
        return global_shortest_pathset, shortest_pathset_record

    def spread_pheronome(self, all_pathset):
        for pathset in all_pathset:
            for path in pathset[0]:
                for move in path:
                    self.pheromone[move] += 1.0/pathset[1]

    def calculate_path_len(self, path):
        s = 0
        for p in path:
            s += self.distances[p]
        s += self.distances[path[-1][1], path[0][0]]
        return s
    
    def calculate_pathset_len(self, paths):
        s=0
        for path in paths:
            s+=self.calculate_path_len(path)
        # s
        return s

    def gen_pathset(self):
        all_paths = []
        paths = self.gen_paths(0)
        # all_paths = [(path, self.calculate_path_len(path)) for path in paths]
        return (paths, self.calculate_pathset_len(paths))


    def gen_paths(self, start):
        paths = [[] for _ in range(self.n_ants)]
        visited = set([start])
        ends = set()
        prevs = [start for _ in range(self.n_ants)]
        
        while len(visited) < self.n_nodes:

            moves = self.pick_moves(visited, ends, prevs)
            for i in range(self.n_ants):
                if moves[i] is not None:
                    paths[i].append((prevs[i], moves[i]))
                else:
                    ends.add(i)
            prevs = moves
            [visited.add(i) if i else None for i in moves]
            # some ants may stop explore
            stop_prob = self.p0*len(visited)/self.n_nodes
            for i in range(self.n_ants):
                if i in ends:
                    continue
                if len(ends)==self.n_ants-1:
                    break
                # print(stop_prob)
                if np.random.rand()<stop_prob:
                    # paths[i].append((prevs[i], start))
                    # print(paths[i])
                    prevs[i]=None
                    ends.add(i)
        return paths
            

    def pick_moves(self, visited, ends, from_nodes):
        '''
        pheromone: (n_nodes,n_nodes)
        distances: (n_nodes,n_nodes)
        visited: set, visited node id
        ends: set, explore end node id
        from_nodes: list, n_ants state, if ant[i] stop explore, from_nodes[i]=None

        return:
        moves: list, len=self.n_ants, if ant[i] stop explore or all nodes were explored, moves[i]=None
        '''
        pheromone = self.pheromone.copy()

        moves = []
        curr_vis = []

        for n in from_nodes:
            if n==None:
                moves.append(None)
            elif len(visited)+len(curr_vis)==self.n_nodes:
                moves.append(None)
            else:
                raw_prob = pheromone[n]
                raw_prob[list(visited) + curr_vis]=0
                raw_prob = raw_prob ** self.alpha * (( 1.0 / self.distances[n]) ** self.beta)
                prob = raw_prob/raw_prob.sum()
                move = int(np.random.choice(self.all_inds, p=prob))
                moves.append(move)
                curr_vis.append(move)
        return moves

