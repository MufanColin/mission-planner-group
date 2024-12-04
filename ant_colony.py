import random as rn
import numpy as np
import progressbar


class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
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
        self.distances = distances  # （n_nodes, n_nodes）
        self.pheromone = np.ones(self.distances.shape) / len(
            distances
        )  # (n_nodes, n_nodes)
        self.all_inds = np.arange(0, len(distances), 1)  # (n_nodes,)
        self.n_best = n_best  # n_best ants spread pheromone
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay  # pheromone decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        """
        Returns:
            final_shortest_path (tuple): (path, path_len)

            shortest_path_record (list): list[(iter_idx, path_len)]

        """
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        shortest_path_record = []
        pbar = progressbar.ProgressBar(maxval=self.n_iterations)(
            range(self.n_iterations)
        )
        for i in pbar:
            all_paths = (
                self.gen_all_paths()
            )  # list[(path, path_len)] path: list[(node_i, node_{i+1})]
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            shortest_path_record.append((i, all_time_shortest_path[1]))
        return all_time_shortest_path, shortest_path_record

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])  # ascending by path_len
        self.pheromone *= self.decay
        for path, dist in sorted_paths[:n_best]:  # n_best ants spread pheromone
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]  # BUG

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # going back to where we started
        return path

    def pick_move(self, pheromone_to, dist_to, visited):
        """
        pheromone: (n_nodes,)
        distances: (n_nodes,)
        visited: set, visited node id
        """
        pheromone_to = np.copy(pheromone_to)
        pheromone_to[list(visited)] = 0

        raw_prob = pheromone_to**self.alpha * ((1.0 / dist_to) ** self.beta)

        prob = raw_prob / raw_prob.sum()  # transition probability
        move = np.random.choice(self.all_inds, p=prob)

        return move
