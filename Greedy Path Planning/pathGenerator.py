import os
from constants import ACTION, DIM, UAVAMOUNT, TIMELENGTH
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
    amountOfUAV = UAVAMOUNT
    POIPosition = list([coordObject(0.3, 0.3), coordObject(0.8, 0.8)])
    POITimes = [2, 5]
    POIList: list[POI] = []
    UAVList: list[UAV] = []
    needyPOI: list[POI] = []
    # POI and UAV creation
    for i in range(len(POIPosition)):
        currPOI = POI(POIPosition[i], POITimes[i], i)
        POIList.append(currPOI)
        needyPOI.append(currPOI)
    for i in range(UAVAMOUNT):
        currUAV = UAV(dims, coordObject(0, 0),
                      heuristic_nefesto(successProbability), i)
        UAVList.append(currUAV)
    # printMapGrid(UAVList, list(
        # map(lambda poi: poi.getSection(dims), POIList)))

    # add randomness to UAV picking POIs
    shuffle(UAVList)
    # Creation of the routes
    for t in range(TIMELENGTH):
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
            # print("------------" + str(uav.id) + "------------")
            # print(list(map(lambda move: move.name, uav.moves)))
            # print(uav.getTarget().id)
            # print("------------------------")

        printMapGrid(UAVList, list(
            map(lambda poi: poi.getSection(dims), POIList)))

    # i want the table to be sorted at the end
    UAVList.sort(key=lambda x: x.id)
    res = []
    for uav in UAVList:
        # print(uav.id)
        res.append(list(map(lambda move: str(move.value), uav.moves)))
        # print(list(map(lambda move: move.name, uav.moves)))
        # print(uav.valuesArray())
    saveMap(res, id, successProbability)
