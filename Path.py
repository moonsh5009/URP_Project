from distance import *

ALPHA = 1.0
BETA = 1.0
N_T = 12


def computeCost(t, N, n, m):
    # return ALPHA * t + BETA * (max(n - N_T * t * N, 1) + m) / N
    return ALPHA * t + BETA * (1 / N_T) * (max(n - N_T * t * N, 1) + m) / N

class Path:
    def __init__(self, ind, time, n):
        self.ind = ind
        self.time = time
        self.m = 0
        self.n = n

    def cost(self, hospScale, m=-1):
        if m > -1:
            return computeCost(self.time, hospScale[self.ind], self.n, m)
        return computeCost(self.time, hospScale[self.ind], self.n, self.m)

    def print(self, hospScale, hosp_info):
        print( self.time, hospScale[self.ind], self.n)
        alltime = str(self.time + (1/N_T) * math.ceil(self.m / hospScale[self.ind]))
        result = '인원: ' + str(self.n) + '/' + str(hospScale[self.ind]) + ', ' + str(self.m) + \
                 ', 코스트: ' + str(self.cost(hospScale, 0)) + '/' + \
                 str(self.cost(hospScale)) + ', 이동시간: ' + \
                 str(self.time) + ', 처리시간: ' + alltime + ', 병원: ' + hosp_info['HosName'][self.ind]
        print(result)