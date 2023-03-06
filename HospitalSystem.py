from Graph import *
from Edges import *
import random


class HospitalSystem:
    def __init__(self, hosp_info):
        self.hosp_info = hosp_info
        self.kdtree = KDTree(hosp_info, 15, 1)
        self.walkEdges = Edge(self.kdtree, TMAP_WALK)
        self.carEdges = Edge(self.kdtree, TMAP_CAR)
        # self.walkEdges.buildNeighbors()
        # self.carEdges.buildNeighbors()
        self.hospNum = len(hosp_info['lat'])

        self.GraphInfo = [[]]
        self.hospScale = hosp_info['capacity']
        # self.hospPatients = [random.randint(10, 100) for i in range(self.hospNum)]
        self.hospPatients = [0 for i in range(self.hospNum)]
        self.hospUpdate = [0 for i in range(self.hospNum)]
        self.hospOperate = hosp_info['operate']
        self.hospTime = hosp_info['time']
        self.Agents = [[] for i in range(self.hospNum)]
        self.sys_time = 0
        self.sys_interval = 0.5

    def hospGraph(self, type):
        if type == TMAP_WALK:
            return self.walkEdges.data['index']
        elif type == TMAP_CAR:
            return self.carEdges.data['index']

    def appendAgents(self, ind, num, startTime, t, position):
        self.Agents[ind].append({'num': num, 'startTime': startTime, 'endTime': startTime + t, 'startPos': position})

    def AddAgents(self, position, num, max_level, type):
        inds, ts = self.kdtree.getNeighborHospitals(position, 5, self.hospTime, self.hospOperate, self.sys_time, type)
        g = Graph(position, inds, ts, self.hospPatients)
        levs = [0, len(g.nodes)]
        maxTime = 0

        for lev in range(max_level - 1):
            for i in range(levs[lev], levs[lev + 1]):
                # Update Graph
                # if self.sys_time - self.hospUdate[g.nodes[i]] > self.sys_interval:
                self.hospUpdate[g.nodes[i]] = self.sys_time
                inds, ts = self.kdtree.getHospitalNeighbors(g.nodes[i], 5, self.hospTime, self.hospOperate, self.sys_time, type)
                self.hospGraph(type)[g.nodes[i]] = inds
                # Add Next Level Hospital
                for adj in self.hospGraph(type)[g.nodes[i]]:
                    if adj not in g.nodes:
                        # t = getWalkTime(position[0], position[1],
                        #                       self.hosp_info['lat'][adj], self.hosp_info['lng'][adj], type)
                        t = addDomainTIme(position[0], position[1],
                                                self.hosp_info['lat'][adj], self.hosp_info['lng'][adj], type)

                        if t > maxTime:
                            maxTime = t
                        if t < 0:
                            continue
                        g.appendPath(adj, t, self.hospPatients[adj])
                        g.nodes.append(adj)
            levs.append(len(g.nodes))
        self.kdtree.appendNearestHospitals(
            position, maxTime, g.nodes, g.paths, self.hospPatients, self.hospTime, self.hospOperate, self.sys_time, type)
        #-----------------------------------------------------
        intersectList = {}
        for i in range(len(g.nodes)):
            n = g.paths[i].ind
            new_time = g.paths[i].time
            if len(self.Agents[n]) > 0:
                self.Agents[n].sort(key=lambda x: x['endTime'])
                for agent in self.Agents[n]:
                    if t < agent['endTime']:
                        old_time = agent['endTime'] - self.sys_time
                        interval_time = old_time - new_time
                        patients = max(g.paths[i].n - (self.hospScale[n] * int(
                            (((agent['endTime'] - agent['startTime'] - interval_time) * 60) / 5))), 0)
                        m = int(interval_time * 60 / 5) * self.hospScale[n]
                        m = 0 if patients > m else m - patients
                        intersectList[n] = m
                        break
                    else:
                        g.paths[i].n += agent['num']
        #-----------------------------------------------------

        g.paths.sort(key=lambda x: x.cost(self.hospScale, 0))
        # self.computePathCeil(g.paths, num, [])
        self.computePathCeil(g.paths, num, intersectList)

        ginfo = []
        for i, p in enumerate(g.paths):
            if p.m > 0:
                tstart = self.sys_time
                tend = self.sys_time + p.time
            else:
                tstart = 0
                tend = 0
            ginfo.append({'index': p.ind, 'scale': self.hospScale[p.ind], 'num': p.m,
                          'cost': p.cost(self.hospScale), 'startTime': tstart, 'endTime': tend, 'startPos': position})

            p.print(self.hospScale, self.hosp_info)
            if p.m > 0:
                self.appendAgents(p.ind, p.m, self.sys_time, p.time, position)
        self.GraphInfo.append(ginfo)
        self.GraphInfo[0].extend(ginfo)

    def computePathCeil(self, ps, m, intersectList=[]):
        vs = []
        if len(ps) <= 0:
            return
        ps[0].m = 0
        for i in range(len(ps) - 1):
            ps[i + 1].m = 0
            vs.append(math.ceil((ps[i + 1].cost(self.hospScale, 0) - ps[i].cost(self.hospScale, 0)) * self.hospScale[
                ps[i].ind] * N_T / BETA))

        for i in range(len(ps)):
            if i < len(ps) - 1:
                plus_ms = vs[i]
                for j in range(i):
                    plus_ms += round(vs[i] * self.hospScale[ps[j].ind] / self.hospScale[ps[i].ind])

                if m > plus_ms:
                    for j in range(i):
                        ps[j].m += round(vs[i] * self.hospScale[ps[j].ind] / self.hospScale[ps[i].ind])
                    ps[i].m += vs[i]
                    if ps[i].ind in intersectList and ps[i].m > intersectList[ps[i].ind]:
                        m += ps[i].m - intersectList[ps[i].ind]
                        ps[i].m = intersectList[ps[i].ind]
                    m -= plus_ms
                    continue

            plus_Ns = self.hospScale[ps[i].ind]
            for j in range(i):
                plus_Ns += self.hospScale[ps[j].ind]

            cm = m
            for j in range(i + 1):
                pm = round(cm * self.hospScale[ps[j].ind] / plus_Ns)
                if ps[j].ind in intersectList and ps[j].m == intersectList[ps[j].ind]:
                    continue
                if m <= pm:
                    ps[j].m += m
                    m = 0
                    break
                ps[j].m += pm
                m -= pm
            if m <= 0:
                break

    def update(self, dt):
        for i in range(self.hospNum):
            currtime = self.sys_time
            spt = dt
            if len(self.Agents[i]) > 0:
                deletes = []
                self.Agents[i].sort(key=lambda x: x['endTime'])
                for j in range(len(self.Agents[i])):
                    if currtime + spt >= self.Agents[i][j]['endTime']:
                        atime = currtime + spt - self.Agents[i][j]['endTime']
                        apatient = self.hospPatients[i] - self.hospScale[i] * atime * 1 / N_T
                        if apatient <= 0:
                            self.hospPatients[i] = self.Agents[i][j]['num']
                        else:
                            self.hospPatients[i] = apatient + self.Agents[i][j]['num']
                        spt -= atime
                        currtime += atime
                        deletes.append(j)

                deletes.reverse()
                for j in deletes:
                    del self.Agents[i][j]

            self.hospPatients[i] = max(self.hospPatients[i] - self.hospScale[i] * spt * N_T, 0)
        self.sys_time += dt
        # print(self.hospPatients[0])
