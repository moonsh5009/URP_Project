import math
import time
import json
import requests

MAX_TMAP = 500

WALK_SPD = 4.0
MAX_WALK_RANGE = 20.0

CAR_SPD = 50.0
MAX_CAR_RANGE = 500.0

TMAP_WALK = 0
TMAP_CAR = 1

def degree2radius(degree):
    return degree * math.pi / 180


def getDistance(lat1, lng1, lat2, lng2):
    earthR = 6371
    dLat = degree2radius(lat2 - lat1)
    dLng = degree2radius(lng2 - lng1)
    a = math.sin(dLat * 0.5) * math.sin(dLat * 0.5) + math.cos(degree2radius(lat1)) * math.cos(
        degree2radius(lat2)) * math.sin(dLng * 0.5) * math.sin(dLng * 0.5)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earthR * c
    return distance

def isLock():
    try:
        with open('bin/Lock.json', 'r', encoding="utf-8") as read_file:
            data = json.load(read_file)
        if data['time'] >= MAX_TMAP:
            return True
    except:
        return False
    return False
def Lock():
    # try:
    #     with open('bin/Lock.json', 'r', encoding="utf-8") as read_file:
    #         data = json.load(read_file)
    # except:
    #     data = {'time': 1}
    #     with open('bin/Lock.json', 'w', encoding="utf-8") as write_file:
    #         json.dump(data, write_file)
    # data['time'] += 1
    # with open('bin/Lock.json', 'w', encoding="utf-8") as write_file:
    #     json.dump(data, write_file)
    return True


def TMapTime(startLat, startLng, endLat, endLng, type):
    # # car
    # walk
    # if isLock():
    #     print("Over ", MAX_TMAP, "!!")
    #     exit(0)

    if type == TMAP_WALK:
        try:
            url = "https://apis.openapi.sk.com/tmap/routes/pedestrian"
            headers = {
                # "appkey": "l7xxbcbc5b58e88e42ef97b859c23fd6e8bf", #나
                "appkey": "l7xx3f5a054e4ce5415591e8ec0abaf942f5", #영찬
                # "appkey": "l7xx64606f6d0f76406f977150b7e9537114", # 동희
                "version": "1",
                "callback": "",
            }

            payload = {
                "roadType": 32,
                "directionOption": 1,
                "startX": startLng,
                "startY": startLat,
                "endX": endLng,
                "endY": endLat,
                "startName": "시작점",
                "endName": "도착점"
            }

            r = requests.post(url, json=payload, headers=headers)

            jsonObj = json.loads(r.text)
            # dist = jsonObj['features'][0]['properties']['totalDistance'] * 0.001
            rtime = jsonObj['features'][0]['properties']['totalTime'] / 3600
            time.sleep(0.1)
            Lock()
        except:
            try:
                if jsonObj['error'] is not None:
                    if jsonObj['error']['message'] == "초당 처리 건수를 초과했습니다.":
                        return -1, None
                    elif jsonObj['error']['message'] == "최대 호출 허용 건수를 초과했습니다.":
                        return -1, None
                    else:
                        Lock()
                        return -1, jsonObj['error']['message']
            except:
                return -2, None
    elif type == TMAP_CAR:
        try:
            url = "https://apis.openapi.sk.com/tmap/routes"
            headers = {
                # "appkey": "l7xxbcbc5b58e88e42ef97b859c23fd6e8bf", #나
                "appkey": "l7xx3f5a054e4ce5415591e8ec0abaf942f5", #영찬
                # "appkey": "l7xx64606f6d0f76406f977150b7e9537114", # 동희
                "version": "1",
                "callback": ""
            }

            payload = {
                "roadType": 32,
                "directionOption": 1,
                "startX": startLng,
                "startY": startLat,
                "endX": endLng,
                "endY": endLat
            }

            r = requests.post(url, json=payload, headers=headers)

            jsonObj = json.loads(r.text)
            # dist = jsonObj['features'][0]['properties']['totalDistance'] * 0.001
            rtime = jsonObj['features'][0]['properties']['totalTime'] /  3600
            time.sleep(0.1)
            Lock()
            # return dist, rtime
        except:
            try:
                if jsonObj['error'] is not None:
                    if jsonObj['error']['message'] == "초당 처리 건수를 초과했습니다.":
                        return -1, None
                    elif jsonObj['error']['message'] == "최대 호출 허용 건수를 초과했습니다.":
                        return -1, None
                    else:
                        Lock()
                        return -1, jsonObj['error']['message']
            except:
                return -2, None
    return rtime, None

def getAddress(str):
    a = str.find('(')
    b = str.find(')')
    if a > -1 and b > -1:
        return str[:a-1] + str[b+1:]
    return str

def getMoveTime(lat0, lng0, lat1, lng1, type):     # return hour
    #----------< T-Map >----------------------------------------------
    if type == TMAP_WALK:
        if getDistance(lat0, lng0, lat1, lng1) > MAX_WALK_RANGE:
            return -1

        tmap, msg = TMapTime(lat0, lng0, lat1, lng1, type)
        if tmap >= 0.0:
            return tmap
    elif type == TMAP_CAR:
        tmap, msg = TMapTime(lat0, lng0, lat1, lng1, type)
        if tmap >= 0.0:
            return tmap
    return -1

def getMoveTime_hosp(i0, i1, hosp_info, type):     # return hour
    #----------< T-Map >----------------------------------------------
    if type == TMAP_WALK:
        if getDistance(hosp_info['lat'][i0], hosp_info['lng'][i0], hosp_info['lat'][i1], hosp_info['lng'][i1]) > MAX_WALK_RANGE:
            return -1
        path = 'bin/WalkTime_Info.json'
    elif type == TMAP_CAR:
        pathbackup = 'bin/WalkTime_Info_backup.json'
        path = 'bin/CarTime_Info.json'
        pathbackup = 'bin/CarTime_Info_backup.json'

    try:
        with open(path, 'r', encoding="utf-8") as read_file:
            data = json.load(read_file)
    except:
        try:
            with open(pathbackup, 'r', encoding="utf-8") as read_file:
                data = json.load(read_file)
        except:
            data = {'time': [[None for i in range(len(hosp_info['lat']))] for i in range(len(hosp_info['lat']))],
                    'error': [[None for i in range(len(hosp_info['lat']))] for i in range(len(hosp_info['lat']))]}
            with open(path, 'w', encoding="utf-8") as write_file:
                json.dump(data, write_file)

    if data['error'][i0][i1] is not None:
        return -1
    if data['time'][i0][i1] is not None:
        return data['time'][i0][i1]

    tmap, msg = TMapTime(hosp_info['lat'][i0], hosp_info['lng'][i0], hosp_info['lat'][i1], hosp_info['lng'][i1], type)
    if tmap >= 0.0:
        print(tmap)
        # data['time'][i0][i1] = data['time'][i1][i0] = tmap
        data['time'][i0][i1] = tmap
        with open(path, 'w', encoding="utf-8") as write_file:
            json.dump(data, write_file)
        with open(pathbackup, 'w', encoding="utf-8") as write_file:
            json.dump(data, write_file)
        return tmap
    elif msg is not None:
        print(msg)
        # data['error'][i0][i1] = data['error'][i1][i0] = msg
        data['error'][i0][i1] = msg
        with open(path, 'w', encoding="utf-8") as write_file:
            json.dump(data, write_file)
        with open(pathbackup, 'w', encoding="utf-8") as write_file:
            json.dump(data, write_file)
    return -1