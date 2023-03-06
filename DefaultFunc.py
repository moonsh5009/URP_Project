from distance import *


def getNearestHospital(hosp_info, position):
    h = 0
    # minDist = getDistance(position[0], position[1], hosp_info.loc[0, 'lat'], hosp_info.loc[0, 'lng'])
    # for i in hosp_info.index:
    #     sub_lat = hosp_info.loc[i, 'lat']
    #     sub_lng = hosp_info.loc[i, 'lng']
    #     curr_dist = getDistance(position[0], position[1], sub_lat, sub_lng)
    #     if curr_dist < minDist:
    #         minDist = curr_dist
    #         h = i
    minDist = getDistance(position[0], position[1], hosp_info['lat'][0], hosp_info['lng'][0])
    for i in range(len(hosp_info['lat'])):
        sub_lat = hosp_info['lat'][i]
        sub_lng = hosp_info['lng'][i]
        curr_dist = getDistance(position[0], position[1], sub_lat, sub_lng)
        if curr_dist < minDist:
            minDist = curr_dist
            h = i
    return [hosp_info['lat'][h], hosp_info['lng'][h]]


def getNearestHospitals(hosp_info, position, range):
    hs = []
    # for i in hosp_info.index:
    #     sub_lat = hosp_info.loc[i, 'lat']
    #     sub_lng = hosp_info.loc[i, 'lng']
    #     if getDistance(position[0], position[1], sub_lat, sub_lng) < range:
    #         hs.append([sub_lat, sub_lng])
    for i in range(len(hosp_info['lat'])):
        sub_lat = hosp_info['lat'][i]
        sub_lng = hosp_info['lng'][i]
        if getDistance(position[0], position[1], sub_lat, sub_lng) < range:
            hs.append([sub_lat, sub_lng])
    return hs