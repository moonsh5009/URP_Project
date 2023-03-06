from KDTree import *


def computeCost(t, N, n, m):
    # return ALPHA * t + BETA * (max(n - N_T * t * N, 1) + m) / N
    return ALPHA * t + BETA * (1 / N_T) * (max(n - N_T * t * N, 1) + m) / N

class Graph:
    def __init__(self, pos, nodes, times, hospitalPatient):
        self.nodes = nodes
        self.paths = []
        for i in range(len(nodes)):
            p = Path(nodes[i], times[i], hospitalPatient[nodes[i]])
            self.paths.append(p)

    def appendPath(self, ind, t, n):
        p = Path(ind, t, n)
        self.paths.append(p)