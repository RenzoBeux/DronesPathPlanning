import os
from constants import ORIGIN
from Obstacle import Obstacle
from constants import DIM, OBSTACLES, POIS, POIS_TIMES, UAVAMOUNT, TIMELENGTH
from random import random, seed, shuffle
from coordObject import coordObject
from POI import POI
from UAV import UAV
from heuristics.ardemisa import heuristic_ardemisa
from heuristics.nefesto import heuristic_nefesto
from utils import *

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
    POIPosition = POIS
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
        # currUAV = UAV(dims, ORIGIN.copy(), obstacles,heuristic_nefesto(successProbability), i)
        currUAV = UAV(dims, ORIGIN.copy(), obstacles,heuristic_ardemisa(), i)
        UAVList.append(currUAV)

    # add randomness to UAV picking POIs
    shuffle(UAVList)

    # qty, rem = divmod(len(UAVList), 4)
    # group1 = UAVList[:(qty+rem)]
    # group2 = UAVList[(qty+rem):(2*qty+rem)]
    # group3 = UAVList[(2*qty+rem):(3*qty+rem)]
    # group4 = UAVList[(3*qty+rem):]
    # Creation of the routes
    UAVList[0].setIsOn(True)
    turnOnProbability = 0.01
    for t in range(TIMELENGTH):
        # increase turnOnProbability exponentially
        turnOnProbability = turnOnProbability * 1.1
        for poi in POIList:
            flag = True
            for uav in UAVList:
                if (uav.getTarget().id == poi.id):
                    flag = False
            if (flag and not(poi in needyPOI) and (t - poi.lastVisit > poi.expectedVisitTime)):
                needyPOI.append(poi)
        for uav in UAVList:
            # Randomly have a chance to set the uav on if it is off
            if (not(uav.isOn) and random() < turnOnProbability):
                uav.setIsOn(True)
            needyPOI = uav.move([t, dims, needyPOI])

    # i want the table to be sorted at the end
    UAVList.sort(key=lambda x: x.id)
    res = []

    for uav in UAVList:
        res.append(list(map(lambda move: str(move.value), uav.moves)))
    saveMap(res, id, successProbability)
