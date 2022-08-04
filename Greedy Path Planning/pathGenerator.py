import os
from Obstacle import Obstacle
from constants import ACTION, DIM, OBSTACLES, POIS, POIS_TIMES, UAVAMOUNT, TIMELENGTH, BIGDIM
from random import randint, random, seed, shuffle
from coordObject import coordObject
from POI import POI
from UAV import UAV
from heuristics.ImoveHeuristic import moveHeuristic
from heuristics.nefesto import heuristic_nefesto
from heuristics.ades import heuristic_ades
from utils import *


def generatePOICoord():
    x = random
    y = random
    return coordObject(x, y)


# this function saves into a txt file an array of arrays of strings
def saveMap(map, id, successProbability):
    # create a folder inside output/
    if not os.path.exists('output/'):
        os.makedirs('output/')
    # create a folder inside output/id/
    if not os.path.exists('output/' + str(int(successProbability*100))):
        os.makedirs('output/' + str(int(successProbability*100)))
    file = open("output/" + str(int(successProbability*100)) +
                "/" + str(id) + ".txt", "w")
    for line in map:
        file.write(" ".join(line) + "\n")
    file.close()


def runGreedy(id, successProbability):
    seed(id)
    dims = DIM
    POIPosition = list(POIS)
    POITimes = POIS_TIMES
    POIList: list[POI] = []
    UAVList: list[UAV] = []
    needyPOI: list[POI] = []
    obstacles: list[Obstacle] = OBSTACLES
    # POI and UAV creation
    for i in range(len(POIPosition)):
        currPOI = POI(POIPosition[i], POITimes[i], i)
        POIList.append(currPOI)
        needyPOI.append(currPOI)
    for i in range(UAVAMOUNT):
        currUAV = UAV(dims, coordObject(0, 0), obstacles,
                      heuristic_nefesto(successProbability), i)
        UAVList.append(currUAV)

    # add randomness to UAV picking POIs
    shuffle(UAVList)
    # Creation of the routes
    for t in range(TIMELENGTH):
        print('TIME:', t)
        # print(UAVList[0].position.x, ' ', UAVList[0].position.y)
        for poi in POIList:
            flag = True
            for uav in UAVList:
                if (uav.getTarget().id == poi.id):
                    flag = False
            if (flag and not(poi in needyPOI) and (t - poi.lastVisit > poi.expectedVisitTime)):
                needyPOI.append(poi)
        for uav in UAVList:
            needyPOI = uav.move([t, dims, needyPOI])

    # i want the table to be sorted at the end
    UAVList.sort(key=lambda x: x.id)
    res = []
    for uav in UAVList:
        res.append(list(map(lambda move: str(move.value), uav.moves)))
    saveMap(res, id, successProbability)
