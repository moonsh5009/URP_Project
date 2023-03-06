import sys
from collections import deque
from Path import *
from DomainSystem import *


class KDNode:
    def __init__(self, minx=0.0, miny=0.0, maxx=0.0, maxy=0.0, level=0):
        self.min = [minx, miny]
        self.max = [maxx, maxy]
        self.level = level
        self.parent = None
        self.childs = [None, None]
        self.divAxis = 0
        self.divPos = 0.0
        self.hospitals = []

    # def __del__(self):
    #     print(self.level)

    def isInside(self, position):
        return self.min[0] <= position[0] <= self.max[0] and self.min[1] <= position[1] <= self.max[1]

    def Min(self, x, y):
        self.min[0] = min(self.min[0], x)
        self.min[1] = min(self.min[1], y)

    def Max(self, x, y):
        self.max[0] = max(self.max[0], x)
        self.max[1] = max(self.max[1], y)

    # def draw(self, vertices, edges):
    #     vs = []
    #     vs.append(self.min)
    #     vs.append([self.min[0], self.max[1]])
    #     vs.append(self.max)
    #     vs.append([self.max[0], self.min[1]])
    #     vertices.append(vs)
    #     if self.childs[0] is None:
    #         for i in range(len(self.hospitals) - 1):
    #             for j in range(i, len(self.hospitals)):
    #                 edges.append([self.hospitals[i], self.hospitals[j]])
    def draw(self, vertices=None):
        if vertices is None:
            return
        vs = []
        vs.append(self.min)
        vs.append([self.min[0], self.max[1]])
        vs.append(self.max)
        vs.append([self.max[0], self.min[1]])
        vertices.append(vs)

    def computeRange(self, pos, range):
        if pos[0] <= self.min[0]:
            lats = [self.max[0]]
        elif pos[0] >= self.max[0]:
            lats = [self.min[0]]
        else:
            lats = [self.min[0], self.max[0]]
        if pos[1] <= self.min[1]:
            lngs = [self.max[1]]
        elif pos[1] >= self.max[1]:
            lngs = [self.min[1]]
        else:
            lngs = [self.min[1], self.max[1]]

        for lng in lngs:
            for lat in lats:
                dist = getDistance(pos[0], pos[1], lat, lng)
                if dist > range:
                    range = dist
        return range


class KDTree:
    def __init__(self, hosp_info, max_level, minimum):
        self.radius = 0
        self.computeNum = 0
        self.hosp_info = hosp_info

        self.root = KDNode(sys.float_info.max, sys.float_info.max,
                           sys.float_info.min, sys.float_info.min, 0)

        for i in range(len(self.hosp_info['lat'])):
            self.root.Min(self.hosp_info['lat'][i], self.hosp_info['lng'][i])
            self.root.Max(self.hosp_info['lat'][i], self.hosp_info['lng'][i])
            self.root.hospitals.append(i)

        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            if node.level >= max_level or len(node.hospitals) <= minimum:
                continue

            proj = [[], []]
            for i in node.hospitals:
                curr_lat = self.hosp_info['lat'][i]
                curr_lng = self.hosp_info['lng'][i]
                if curr_lat not in proj[0]:
                    proj[0].append(curr_lat)
                if curr_lng not in proj[1]:
                    proj[1].append(curr_lng)

            if len(proj[0]) <= minimum and len(proj[1]) <= minimum:
                continue

            node.divAxis = int(max(proj[0]) - min(proj[0]) < max(proj[1]) - min(proj[1]))
            # proj[node.divAxis].sort()
            # node.divPos = proj[node.divAxis][len(proj[node.divAxis]) // 2]
            node.divPos = 0
            for i in node.hospitals:
                if node.divAxis == 0:
                    node.divPos += self.hosp_info['lat'][i]
                else:
                    node.divPos += self.hosp_info['lng'][i]
            node.divPos /= len(node.hospitals)

            node.childs[0] = KDNode(node.min[0], node.min[1], node.max[0], node.max[1], node.level + 1)
            node.childs[1] = KDNode(node.min[0], node.min[1], node.max[0], node.max[1], node.level + 1)
            node.childs[0].max[node.divAxis] = node.childs[1].min[node.divAxis] = node.divPos
            node.childs[0].parent = node.childs[1].parent = node
            for i in node.hospitals:
                if node.divAxis == 0:
                    if self.hosp_info['lat'][i] < node.divPos:
                        node.childs[0].hospitals.append(i)
                    else:
                        node.childs[1].hospitals.append(i)
                else:
                    if self.hosp_info['lng'][i] < node.divPos:
                        node.childs[0].hospitals.append(i)
                    else:
                        node.childs[1].hospitals.append(i)
            node.hospitals = []

            if node.childs[0] is not None:
                queue.append(node.childs[0])
                queue.append(node.childs[1])

    def projection(self, position):
        if self.root.isInside(position):
            return position
        pos = [position[0], position[1]]
        if self.root.min[0] > pos[0]:
            pos[0] = self.root.min[0]
        elif self.root.max[0] < pos[0]:
            pos[0] = self.root.max[0]
        if self.root.min[1] > pos[1]:
            pos[1] = self.root.min[1]
        elif self.root.max[1] < pos[1]:
            pos[1] = self.root.max[1]
        return pos

    def intersact(self, node, position, range):
        lat = position[0]
        lng = position[1]
        if node.min[0] > position[0]:
            lat = node.min[0]
        elif node.max[0] < position[0]:
            lat = node.max[0]
        if node.min[1] > position[1]:
            lng = node.min[1]
        elif node.max[1] < position[1]:
            lng = node.max[1]
        return getDistance(lat, lng, position[0], position[1]) <= range

    def getNearestNode(self, position):
        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            if node.childs[0] is None:
                return node
            if position[node.divAxis] > node.divPos:
                queue.append(node.childs[1])
            else:
                queue.append(node.childs[0])
        return None

    def getNearestHospital(self, position):
        proj_pos = self.projection(position)
        nearestNode = self.getNearestNode(proj_pos)
        if nearestNode is None:
            return -1

        minDist = sys.float_info.max
        nearestH = -1
        for i in nearestNode.hospitals:
            dist = getDistance(self.hosp_info['lat'][i], self.hosp_info['lng'][i], position[0], position[1])
            if minDist > dist:
                minDist = dist
                nearestH = i

        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            if not self.intersact(node, proj_pos, minDist):
                continue

            if node.childs[0] is None:
                if node is nearestNode:
                    continue
                for i in node.hospitals:
                    dist = getDistance(self.hosp_info['lat'][i], self.hosp_info['lng'][i], position[0], position[1])
                    if minDist > dist:
                        minDist = dist
                        nearestH = i
            else:
                queue.append(node.childs[0])
                queue.append(node.childs[1])

        return nearestH

    def getNearestHospitals(self, position, range):
        nearestHs = []
        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            if not self.intersact(node, position, range):
                continue

            if node.childs[0] is None:
                for i in node.hospitals:
                    dist = getDistance(self.hosp_info['lat'][i], self.hosp_info['lng'][i], position[0], position[1])
                    if dist <= range:
                        nearestHs.append(i);
            else:
                queue.append(node.childs[0])
                queue.append(node.childs[1])

        return nearestHs

    def appendNearestHospitals(self, position, maxTime, inds, paths, hostpitalPatients, hospTime, hospOperate, sys_time, type):
        nearestinds = []
        nearestts = []
        if type == TMAP_WALK:
            mrange = maxTime * WALK_SPD
        elif type == TMAP_CAR:
            mrange = maxTime * CAR_SPD

        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            if not self.intersact(node, position, mrange):
                continue

            if node.childs[0] is None:
                for i in node.hospitals:
                    if i not in inds:
                        dist = getDistance(self.hosp_info['lat'][i], self.hosp_info['lng'][i], position[0], position[1])
                        if dist <= mrange:
                            # if hospOperate[i] is False or sys_time < hospTime[i][0] or sys_time > hospTime[i][1]:
                            #     continue
                            t = addDomainTIme(position[0], position[1], self.hosp_info['lat'][i], self.hosp_info['lng'][i], type)
                            self.computeNum += 1
                            print(i, t, maxTime)
                            if t <= maxTime:
                                if len(nearestinds) == 0:
                                    nearestinds.append(i)
                                    nearestts.append(t)
                                    continue
                                for j in range(len(nearestinds)):
                                    if t < nearestts[j]:
                                        nearestinds.insert(j, i)
                                        nearestts.insert(j, t)
                                        break
                                    if j == len(nearestinds) - 1:
                                        nearestinds.append(i)
                                        nearestts.append(t)
            else:
                queue.append(node.childs[0])
                queue.append(node.childs[1])
        for i in range(len(nearestinds)):
            paths.append(Path(nearestinds[i], nearestts[i], hostpitalPatients[nearestinds[i]]))
        print(self.computeNum)

    def getNeighborHospitals(self, position, depth, hospTime, hospOperate, sys_time, type):  # 환자
        if depth <= 0:
            print("Error depth")
            return
        nearestNode = self.getNearestNode(self.projection(position))
        if nearestNode is None:
            return -1

        visitedNodes = [nearestNode]
        nearestHs = []
        distHs = []
        for i in nearestNode.hospitals:
            dist = getDistance(position[0], position[1], self.hosp_info['lat'][i], self.hosp_info['lng'][i])
            distHs.append((i, dist))

        s_range = nearestNode.computeRange(position, 0)
        while len(nearestHs) < depth:
            curr_range = s_range
            queue = deque([self.root])
            while len(queue):
                node = queue.popleft()
                if not self.intersact(node, position, curr_range):
                    continue
                if node.childs[0] is None:
                    if node in visitedNodes:
                        continue
                    visitedNodes.append(node)
                    s_range = node.computeRange(position, s_range)
                    for i in node.hospitals:
                        dist = getDistance(position[0], position[1], self.hosp_info['lat'][i], self.hosp_info['lng'][i])
                        if len(distHs) == 0:
                            distHs.append((i, dist))
                            continue
                        for j in range(len(distHs)):
                            if dist < distHs[j][1]:
                                distHs.insert(j, (i, dist))
                                break
                            if j == len(distHs) - 1:
                                distHs.append((i, dist))
                else:
                    queue.append(node.childs[0])
                    queue.append(node.childs[1])
            print(len(distHs))

            for h in distHs:
                if len(nearestHs) < depth:
                    # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                    #     continue
                    # t = getWalkTime(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]])
                    t = addDomainTIme(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]], type)
                    self.computeNum += 1
                    if t < 0:
                        continue
                    if len(nearestHs) == 0:
                        nearestHs.append((h[0], t))
                        continue
                    for i in range(len(nearestHs)):
                        if t < nearestHs[i][1]:
                            nearestHs.insert(i, (h[0], t))
                            break
                        if i == len(nearestHs) - 1:
                            nearestHs.append((h[0], t))
                    if len(nearestHs) == depth:
                        if type == TMAP_WALK:
                            minDist = nearestHs[depth - 1][1] * WALK_SPD
                        elif type == TMAP_CAR:
                            minDist = nearestHs[depth - 1][1] * CAR_SPD
                else:
                    if h[1] > minDist:
                        break
                    # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                    #     continue
                    # t = getWalkTime(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]])
                    t = addDomainTIme(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]], type)
                    self.computeNum += 1
                    if t == -1:
                        continue
                    for i in range(depth):
                        if t < nearestHs[i][1]:
                            nearestHs.insert(i, (h[0], t))
                            if type == TMAP_WALK:
                                minDist = nearestHs[depth - 1][1] * WALK_SPD
                            elif type == TMAP_CAR:
                                minDist = nearestHs[depth - 1][1] * CAR_SPD
                            break
            print(nearestHs)
            if type == TMAP_WALK:
                if curr_range >= MAX_WALK_RANGE:
                    break
            elif type == TMAP_CAR:
                if curr_range >= MAX_CAR_RANGE:
                    break
            distHs.clear()

        if len(nearestHs) <= 0:
            return [], []
        elif len(nearestHs) >= depth:
            if type == TMAP_WALK:
                curr_range = nearestHs[depth - 1][1] * WALK_SPD
            elif type == TMAP_CAR:
                curr_range = nearestHs[depth - 1][1] * CAR_SPD
        else:
            if type == TMAP_WALK:
                curr_range = nearestHs[len(nearestHs) - 1][1] * WALK_SPD
            elif type == TMAP_CAR:
                curr_range = nearestHs[len(nearestHs) - 1][1] * CAR_SPD

        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            if not self.intersact(node, position, curr_range):
                continue
            if node.childs[0] is None:
                if node in visitedNodes:
                    continue
                visitedNodes.append(node)
                for i in node.hospitals:
                    dist = getDistance(position[0], position[1], self.hosp_info['lat'][i], self.hosp_info['lng'][i])
                    if len(distHs) == 0:
                        distHs.append((i, dist))
                        continue
                    for j in range(len(distHs)):
                        if dist < distHs[j][1]:
                            distHs.insert(j, (i, dist))
                            break
                        if j == len(distHs) - 1:
                            distHs.append((i, dist))
            else:
                queue.append(node.childs[0])
                queue.append(node.childs[1])
        # print(index, distHs)

        for h in distHs:
            if len(nearestHs) < depth:
                # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                #     continue
                # t = getWalkTime(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]])
                t = addDomainTIme(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]], type)
                self.computeNum += 1
                if t == -1:
                    continue
                if len(nearestHs) == 0:
                    nearestHs.append((h[0], t))
                    continue
                for i in range(len(nearestHs)):
                    if t < nearestHs[i][1]:
                        nearestHs.insert(i, (h[0], t))
                        break
                    if i == len(nearestHs) - 1:
                        nearestHs.append((h[0], t))
                if len(nearestHs) == depth:
                    if type == TMAP_WALK:
                        minDist = nearestHs[depth - 1][1] * WALK_SPD
                    elif type == TMAP_CAR:
                        minDist = nearestHs[depth - 1][1] * CAR_SPD
            else:
                if h[1] > minDist:
                    break
                # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                #     continue
                # t = getWalkTime(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]])
                t = addDomainTIme(position[0], position[1], self.hosp_info['lat'][h[0]], self.hosp_info['lng'][h[0]], type)
                self.computeNum += 1
                if t == -1:
                    continue
                for i in range(depth):
                    if t < nearestHs[i][1]:
                        nearestHs.insert(i, (h[0], t))
                        if type == TMAP_WALK:
                            minDist = nearestHs[depth - 1][1] * WALK_SPD
                        elif type == TMAP_CAR:
                            minDist = nearestHs[depth - 1][1] * CAR_SPD
                        break

        print("computeNum: " + str(self.computeNum))
        inds = []
        ts = []
        for h in nearestHs:
            inds.append(h[0])
            ts.append(h[1])
            if len(inds) >= depth:
                break
        return inds, ts

    def getHospitalNeighbors(self, index, depth, hospTime, hospOperate, sys_time, type):
        if depth <= 0:
            print("Error depth")
            return
        pos = [self.hosp_info['lat'][index], self.hosp_info['lng'][index]]
        nearestNode = self.getNearestNode(pos)
        if nearestNode is None:
            return -1

        visitedNodes = [nearestNode]
        nearestHs = []
        distHs = []
        for i in nearestNode.hospitals:
            if i == index:
                continue
            dist = getDistance(pos[0], pos[1], self.hosp_info['lat'][i], self.hosp_info['lng'][i])
            distHs.append((i, dist))

        s_range = nearestNode.computeRange(pos, 0)
        while len(nearestHs) < depth:
            curr_range = s_range
            queue = deque([self.root])
            while len(queue):
                node = queue.popleft()
                if not self.intersact(node, pos, curr_range):
                    continue
                if node.childs[0] is None:
                    if node in visitedNodes:
                        continue
                    visitedNodes.append(node)
                    s_range = node.computeRange(pos, s_range)
                    for i in node.hospitals:
                        dist = getDistance(pos[0], pos[1], self.hosp_info['lat'][i], self.hosp_info['lng'][i])
                        if len(distHs) == 0:
                            distHs.append((i, dist))
                            continue
                        for j in range(len(distHs)):
                            if dist < distHs[j][1]:
                                distHs.insert(j, (i, dist))
                                break
                            if j == len(distHs) - 1:
                                distHs.append((i, dist))
                else:
                    queue.append(node.childs[0])
                    queue.append(node.childs[1])

            for h in distHs:
                if len(nearestHs) < depth:
                    # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                    #     continue

                    # t = getMoveTime_hosp(index, h[0], self.hosp_info, type)
                    t = addDomainTIme_hosp(index, h[0], self.hosp_info, type)
                    self.computeNum += 1
                    if t < 0:
                        # print(index, h[0], "dndjdl")
                        continue
                    if len(nearestHs) == 0:
                        nearestHs.append((h[0], t))
                        continue
                    for i in range(len(nearestHs)):
                        if t < nearestHs[i][1]:
                            nearestHs.insert(i, (h[0], t))
                            break
                        if i == len(nearestHs) - 1:
                            nearestHs.append((h[0], t))
                    if len(nearestHs) == depth:
                        if type == TMAP_WALK:
                            minDist = nearestHs[depth - 1][1] * WALK_SPD
                        elif type == TMAP_CAR:
                            minDist = nearestHs[depth - 1][1] * CAR_SPD
                else:
                    if h[1] > minDist:
                        break
                    # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                    #     continue

                    # t = getMoveTime_hosp(index, h[0], self.hosp_info, type)
                    t = addDomainTIme_hosp(index, h[0], self.hosp_info, type)
                    self.computeNum += 1
                    if t < 0:
                        # print(index, h[0], "dndjdl")
                        continue
                    for i in range(depth):
                        if t < nearestHs[i][1]:
                            nearestHs.insert(i, (h[0], t))
                            if type == TMAP_WALK:
                                minDist = nearestHs[depth - 1][1] * WALK_SPD
                            elif type == TMAP_CAR:
                                minDist = nearestHs[depth - 1][1] * CAR_SPD
                            break
            if type == TMAP_WALK:
                if curr_range >= MAX_WALK_RANGE:
                    break
            elif type == TMAP_CAR:
                if curr_range >= MAX_CAR_RANGE:
                    break
                # break
            distHs.clear()

        if len(nearestHs) <= 0:
            return [], []
        elif len(nearestHs) >= depth:
            if type == TMAP_WALK:
                curr_range = nearestHs[depth - 1][1] * WALK_SPD
            elif type == TMAP_CAR:
                curr_range = nearestHs[depth - 1][1] * CAR_SPD
        else:
            if type == TMAP_WALK:
                curr_range = nearestHs[len(nearestHs) - 1][1] * WALK_SPD
            elif type == TMAP_CAR:
                curr_range = nearestHs[len(nearestHs) - 1][1] * CAR_SPD

        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            if not self.intersact(node, pos, curr_range):
                continue
            if node.childs[0] is None:
                if node in visitedNodes:
                    continue
                visitedNodes.append(node)
                for i in node.hospitals:
                    dist = getDistance(pos[0], pos[1], self.hosp_info['lat'][i], self.hosp_info['lng'][i])
                    if len(distHs) == 0:
                        distHs.append((i, dist))
                        continue
                    for j in range(len(distHs)):
                        if dist < distHs[j][1]:
                            distHs.insert(j, (i, dist))
                            break
                        if j == len(distHs) - 1:
                            distHs.append((i, dist))
            else:
                queue.append(node.childs[0])
                queue.append(node.childs[1])
        # print(index, distHs)

        for h in distHs:
            if len(nearestHs) < depth:
                # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                #     continue

                # t = getMoveTime_hosp(index, h[0], self.hosp_info, type)
                t = addDomainTIme_hosp(index, h[0], self.hosp_info, type)
                self.computeNum += 1
                if t < 0:
                    # print(index, h[0], "dndjdl")
                    continue
                if len(nearestHs) == 0:
                    nearestHs.append((h[0], t))
                    continue
                for i in range(len(nearestHs)):
                    if t < nearestHs[i][1]:
                        nearestHs.insert(i, (h[0], t))
                        break
                    if i == len(nearestHs) - 1:
                        nearestHs.append((h[0], t))
                if len(nearestHs) == depth:
                    if type == TMAP_WALK:
                        minDist = nearestHs[depth - 1][1] * WALK_SPD
                    elif type == TMAP_CAR:
                        minDist = nearestHs[depth - 1][1] * CAR_SPD
            else:
                if h[1] > minDist:
                    break
                # if hospOperate[h[0]] is False or sys_time < hospTime[h[0]][0] or sys_time > hospTime[h[0]][1]:
                #     continue

                # t = getMoveTime_hosp(index, h[0], self.hosp_info, type)
                t = addDomainTIme_hosp(index, h[0], self.hosp_info, type)
                self.computeNum += 1
                if t < 0:
                    # print(index, h[0], "dndjdl")
                    continue
                for i in range(depth):
                    if t < nearestHs[i][1]:
                        nearestHs.insert(i, (h[0], t))
                        if type == TMAP_WALK:
                            minDist = nearestHs[depth - 1][1] * WALK_SPD
                        elif type == TMAP_CAR:
                            minDist = nearestHs[depth - 1][1] * CAR_SPD
                        break

        print("computeNum: " + str(self.computeNum))
        inds = []
        ts = []
        for h in nearestHs:
            inds.append(h[0])
            ts.append(h[1])
            if len(inds) >= depth:
                break
        return inds, ts

    def draw(self, vertices):
        if vertices is None or self.root is None:
            return

        queue = deque([self.root])
        while len(queue):
            node = queue.popleft()
            node.draw(vertices)
            if node.childs[0] is not None:
                queue.append(node.childs[0])
                queue.append(node.childs[1])

