from distance import *

YesOrNo = True

with open('bin/hospitals_Info.json', 'r', encoding="utf-8") as read_file:
    hosp_info = json.load(read_file)

# domainPath = 'bin/Domain_Seoul_walk.json'
domainPath = 'bin/Domain_Seoul_car.json'
# domainPath = 'bin/Domain_Seoul_car_OffTime.json'

# domainPath = 'bin/Domain_Busan_car.json'
# domainPath = 'bin/Domain_Busan_car_OffTime.json'

# domainPath = 'bin/Domain_Geoje_car.json'
# domainPath = 'bin/Domain_Geoje_car_OffTime.json'
# domainPath = 'bin/Domain_Pyeongchang_car.json'
# domainPath = 'bin/Domain_Pyeongchang_car_OffTime.json'
# domainPath = 'bin/Domain_Mokpo_car.json'
# domainPath = 'bin/Domain_Mokpo_car_OffTime.json'
# domainPath = 'bin/Domain_Goseong_car.json'
# domainPath = 'bin/Domain_Goseong_car_OffTime.json'

domainData = [0, None];

try:
    with open(domainPath, 'r', encoding="utf-8") as read_file:
        domainData[1] = json.load(read_file)
except:
    domainData[1] = {'time': [None for i in range(100000)]}
    with open(domainPath, 'w', encoding="utf-8") as write_file:
        json.dump(domainData[1], write_file)

def addDomainTIme(lat0, lng0, lat1, lng1, type):
    if YesOrNo:
        ind = domainData[0]
        print(ind, domainData[1]['time'][ind])
        if domainData[1]['time'][ind] is None:
            t = getMoveTime(lat0, lng0, lat1, lng1, type)
            if t < 0:
                domainData[0] += 1
                return -1
            domainData[1]['time'][ind] = t
            with open(domainPath, 'w', encoding="utf-8") as write_file:
                json.dump(domainData[1], write_file)
        domainData[0] += 1
        return domainData[1]['time'][ind]
    t = getMoveTime(lat0, lng0, lat1, lng1, type)
    print(t)
    return t

def addDomainTIme_hosp(i0, i1, hosp_info, type):
    if YesOrNo:
        ind = domainData[0]
        print(ind, domainData[1]['time'][ind])
        if domainData[1]['time'][ind] is None:
            t = getMoveTime_hosp(i0, i1, hosp_info, type)
            if t < 0:
                domainData[0] += 1
                return -1
            domainData[1]['time'][ind] = t
            with open(domainPath, 'w', encoding="utf-8") as write_file:
                json.dump(domainData[1], write_file)
        domainData[0] += 1
        return domainData[1]['time'][ind]
    t = getMoveTime_hosp(i0, i1, hosp_info, type)
    print(t)
    return t