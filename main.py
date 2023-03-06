import time
from flask import *
from HospitalSystem import *

hosSystem = HospitalSystem(hosp_info)

# currLat = 37.5166119773031
# currLng = 127.041258693516
global currLat
global currLng
global step

# seoul
currLat = 37.608279047695646
currLng = 126.979614395164597

# busan
# currLat = 35.11601485006819
# currLng = 129.04202842329627

# Jeju
# currLat = 36.10632999298861
# currLng = 127.09829801511857

# pyeongchang
# currLat = 37.65931851276612
# currLng = 128.6942586824982

# Mokpo
# currLat = 34.809304
# currLng = 126.403373

# Goseong
# currLat = 38.37945335531811
# currLng = 128.4790438151533

step = 0

app = Flask(__name__)
app.secret_key = 'a4p53og4jiv9240t923lk41i2jp5t'

@app.route('/')
def home():
    return render_template('Map.html',
                           startLat=currLat, startLng=currLng,
                           hospitals=hosp_info)


@app.route('/addAgents', methods=["POST"])
def addAgents():
    data = json.loads(request.data)
    currLat = data.get('lat')
    currLng = data.get('lng')
    # currLat = 37.63016881950865
    # currLng = 127.03761114037421

    timer = time.time()
    # hosSystem.AddAgents([currLat, currLng], 2000, 3)

    print("Set:", time.time() - timer, " sec")

    return jsonify({"hospPatients": hosSystem.hospPatients, "Agents": hosSystem.Agents, "GraphInfo": hosSystem.GraphInfo})

ppap = []
@app.route('/update', methods=["POST"])
def updateSimulation():
    data = json.loads(request.data)
    # currLat = 37.63016881950865
    # currLng = 127.03761114037421

    timer = time.time()
    hosSystem.update(data.get('dt'))
    print("Update:", time.time() - timer, " sec")
    print("System Time:", hosSystem.sys_time, " sec")

    # ppap.append(hosSystem.PatientsNum())
    # with open('bin/none.json', 'w', encoding="utf-8") as write_file:
    #     json.dump(ppap, write_file)
    # print('ppap', hosSystem.PatientsNum())

    global step
    if step == 0:
        if hosSystem.sys_time >= 0.3:
            step += 1

    return jsonify({"time": hosSystem.sys_time, "hospPatients": hosSystem.hospPatients,
                    "Agents": hosSystem.Agents, "GraphInfo": hosSystem.GraphInfo})


if __name__ == '__main__':
    # with open('bin/WalkTime_Info.json', 'r', encoding="utf-8") as read_file:
    #     data = json.load(read_file)
    # for i in range(len(data['error'])):
    #     for j in range(len(data['error'][i])):
    #         if data['error'][i][j] is not None:
    #             # print(i, j, data['error'][i][j])
    #             print(hosp_info['HosName'][i], hosp_info['HosName'][j], data['error'][i][j])
    # with open('bin/error_hos.json', 'r', encoding="utf-8") as read_file:
    #     errindex = json.load(read_file)

    # Domain0_walk
    # Domain0_walk 174
    # hosSystem.AddAgents([37.54477427445537, 126.9675917719589], 1000, 2, TMAP_WALK)
    # hosSystem.AddAgents([37.56492303196376, 126.949014605731], 1000, 2, TMAP_WALK)
    # hosSystem.AddAgents([37.55516422740225, 126.97335343369602], 1000, 2, TMAP_WALK)
    # print(domainData[0])

    # Seoul
    hosSystem.AddAgents([37.54477427445537, 126.9675917719589], 2000, 2, TMAP_CAR)
    hosSystem.AddAgents([37.56492303196376, 126.949014605731], 2000, 2, TMAP_CAR)
    hosSystem.AddAgents([37.55516422740225, 126.97335343369602], 2000, 2, TMAP_CAR)

    # Busan
    # hosSystem.AddAgents([35.11601485006819, 129.04202842329627], 2000, 2, TMAP_CAR)     #부산역
    # hosSystem.AddAgents([35.14228181173271, 129.10140829972366], 2000, 2, TMAP_CAR)     #대연 힐스테이트
    # hosSystem.AddAgents([35.08788687896651, 129.05959634024745], 2000, 2, TMAP_CAR)     #세앙쉬에당아파트

    # GeojeIsland
    # hosSystem.AddAgents([34.86905064961647, 128.7313043575815], 2000, 2, TMAP_CAR)  # 우진빌라아파트
    # hosSystem.AddAgents([34.881387794095865, 128.62571036493216], 2000, 2, TMAP_CAR)  # 거원아파트
    # hosSystem.AddAgents([34.88978661026856, 128.60629213385153], 2000, 2, TMAP_CAR)  # 장평코아루아파트
    # hosSystem.AddAgents([34.73988581550952, 128.66363331459073], 2000, 2, TMAP_CAR)  # 해금강블루마을리조트
    # hosSystem.AddAgents([34.860646473980644, 128.52561826137563], 2000, 2, TMAP_CAR)  # 산방산비원

    # Pyeongchang
    # hosSystem.AddAgents([37.65931851276612, 128.6942586824982], 2000, 2, TMAP_CAR)      # 평창 올림픽 선수촌
    # hosSystem.AddAgents([37.65829412656946, 128.66978071894894], 2000, 2, TMAP_CAR)     # 인터컨티넨탈 알펜시아 평창리조트
    # hosSystem.AddAgents([37.64291709908886, 128.68012829927267], 2000, 2, TMAP_CAR)     # 용평리조트 스키장

    # Mokpo
    # hosSystem.AddAgents([34.809304, 126.403373], 2000, 2, TMAP_CAR)                       # 목포대학교 목포캠퍼스
    # hosSystem.AddAgents([34.80062022330291, 126.4072735791103], 2000, 2, TMAP_CAR)        # 목포 금호타운아파트
    # hosSystem.AddAgents([34.80474844320843, 126.39284883918583], 2000, 2, TMAP_CAR)       # 목포 목양교

    # Goseong
    # hosSystem.AddAgents([38.37945335531811, 128.4790438151533], 2000, 2, TMAP_CAR)          # 고성삼익아파트
    # hosSystem.AddAgents([38.374409384238774, 128.50575557430088], 2000, 2, TMAP_CAR)        # 솔밭펜션
    # hosSystem.AddAgents([38.24252025733896, 128.53753687762747], 2000, 2, TMAP_CAR)         # 파인리즈리조트아젤리아스파
    # hosSystem.AddAgents([38.31140789004759, 128.51149559417513], 2000, 2, TMAP_CAR)         # 설악썬벨리리조트

    # 사량도
    # 사량여인숙 34.844514706491736, 128.22351401464545
    # 사량초등학교 34.83937175088894, 128.1808627643408

    print(domainData[0])

    app.run(port=8080)

    # latlng 최신화
    # print(hosp_info['address'][0])
    # data = {'latlng': [], 'newlatlng': [], 'newlatlngEntr': []}
    # for i in range(len(hosp_info['address'])):
    #     fullAddr = hosp_info['address'][i]
    #     url = "https://apis.openapi.sk.com/tmap/geo/fullAddrGeo"
    #
    #     headers = {
    #         "vertsion": 1,
    #         "formal": "json",
    #         "callback": "result",
    #         # "appkey": "l7xx3f5a054e4ce5415591e8ec0abaf942f5",  # 영찬
    #         "appkey": "l7xxbcbc5b58e88e42ef97b859c23fd6e8bf", #나
    #         "fullAddr" : fullAddr,
    #         "addresssFlag": "F00",
    #         "coordType": "WGS84GEO"
    #     }
    #
    #     r = requests.post(url, headers)
    #     path = 'bin/Latlng_Info.json'
    #     jsonObj = json.loads(r.text)
    #     try:
    #         data['latlng'].append([jsonObj['coordinateInfo']['coordinate'][0]['lat'], jsonObj['coordinateInfo']['coordinate'][0]['lon']])
    #         data['newlatlng'].append([jsonObj['coordinateInfo']['coordinate'][0]['newLat'], jsonObj['coordinateInfo']['coordinate'][0]['newLon']])
    #         data['newlatlngEntr'].append([jsonObj['coordinateInfo']['coordinate'][0]['newLatEntr'], jsonObj['coordinateInfo']['coordinate'][0]['newLonEntr']])
    #
    #         with open(path, 'w', encoding="utf-8") as write_file:
    #             json.dump(data, write_file)
    #     except:
    #         print(jsonObj)
    #     print(i, " done")

    # hospinfo 최신화
    # path = 'bin/Latlng_Info.json'
    # newpath = 'bin/new_hospitals_Info.json'
    # newhosp_info = {"HosName":["" for i in range(len(hosp_info['lat']))], "address":["" for i in range(len(hosp_info['lat']))],
    #                 "lng":[-1 for i in range(len(hosp_info['lat']))], "lat":[-1 for i in range(len(hosp_info['lat']))],
    #                 "capacity":["" for i in range(len(hosp_info['lat']))]}
    # with open(path, 'r', encoding="utf-8") as read_file:
    #     data = json.load(read_file)
    #
    # for i in range(len(hosp_info['lat'])):
    #     newhosp_info['HosName'][i] = hosp_info['HosName'][i]
    #     newhosp_info['address'][i] = hosp_info['address'][i]
    #     oldlatlng = [hosp_info['lat'][i], hosp_info['lng'][i]]
    #     if data['latlng'][i][0] != '':
    #         newlatlng = [data['latlng'][i][0], data['latlng'][i][1]]
    #     elif data['newlatlng'][i][0] != '':
    #         newlatlng = [data['newlatlng'][i][0], data['newlatlng'][i][1]]
    #     else:
    #         newlatlng = [data['newlatlngEntr'][i][0], data['newlatlngEntr'][i][1]]
    #     print('old', oldlatlng, ', new', newlatlng)
    #     newhosp_info['lat'][i] = float(newlatlng[0])
    #     newhosp_info['lng'][i] = float(newlatlng[1])
    #     newhosp_info['capacity'][i] = hosp_info['capacity'][i]
    #
    # with open(newpath, 'w', encoding="utf-8") as write_file:
    #     json.dump(newhosp_info, write_file) # , indent=5, sort_keys=True)
