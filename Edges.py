import json
from distance import *


class Edge:
    def __init__(self, tree, type):
        if type == TMAP_WALK:
            self.path = 'bin/Neighbors_Info_walk.json'
        elif type == TMAP_CAR:
            self.path = 'bin/Neighbors_Info_car.json'
        self.tree = tree
        self.type = type
        try:
            with open(self.path, 'r', encoding="utf-8") as read_file:
                self.data = json.load(read_file)
            print(self.data)
        except:
            self.data = {"index": [[] for i in range(len(tree.hosp_info['lat']))]}
            with open(self.path, 'w', encoding="utf-8") as write_file:
                json.dump(self.data, write_file)

    def buildNeighbors(self):
        for i in range(len(self.tree.hosp_info['lat'])):
            inds, ts = self.tree.getHospitalNeighbors(
                i, 5, self.tree.hosp_info['time'], self.tree.hosp_info['operate'], 15, self.type)

            self.data['index'][i] = inds
            # 중간저장
            # with open(path, 'w', encoding="utf-8") as write_file:
            #     json.dump(data, write_file)
            print(str(i) + " Done")

        with open(self.path, 'w', encoding="utf-8") as write_file:
            json.dump(self.data, write_file)

    # def exceptEdges(self, tolerance):
    #     with open('bin/WalkTime_Info.json', 'r', encoding="utf-8") as read_file:
    #         times = json.load(read_file)['time']
    #
    #     for i in range(len(self.tree.hosp_info['lat'])):
    #         for nei in self.data['index'][i]:
    #             for neinei in self.data['index'][nei]:
    #                 if neinei in self.data['index'][i]:
    #                     # print(times[i][neinei] , times[i][nei], times[nei][neinei])
    #                     if times[i][neinei] is not None and times[i][nei] is not None and times[nei][neinei] is not None:
    #                         if times[i][neinei] + tolerance >= times[i][nei] + times[nei][neinei]:
    #                             self.data['index'][i].remove(neinei)
    #
    #     with open('bin/Edges_Info.json', 'w', encoding="utf-8") as write_file:
    #         json.dump(self.data, write_file)