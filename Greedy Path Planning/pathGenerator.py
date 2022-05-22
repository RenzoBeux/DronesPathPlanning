from constants import *
from classes import *
from utils import *
from random import random, seed

def generatePOICoord():
    x = random
    y = random
    return coordObject(x,y)

if __name__ =="__main__":
    seed(0)
    base = coordObject(0,0)
    dims = DIM
    amountOfUAV = UAVAMOUNT
    POIPosition = [coordObject(0.5,0.5)]
    POITimes = [10]
    POIList:list[POI] = []
    UAVList:list[UAV] = []
    needyPOI:list[POI] = []
    printMapGrid(base,POIPosition)
    # POI and UAV creation
    for i in range(POIAMOUNT):
        currPOI = POI(POIPosition[i],POITimes[i])
        POIList.append(currPOI)
        needyPOI.append(currPOI)
    for i in range(UAVAMOUNT):
        currUAV = UAV(dims,base)
        UAVList.append(currUAV)
    # Creation of the routes
    for t in range(TIMELENGTH):
        print(UAVList[0].position.x,' ',UAVList[0].position.y)
        for poi in POIList:
            if (not(poi in needyPOI) and (t - poi.lastVisit > poi.expectedVisitTime)):
                needyPOI.append()
        for uav in UAVList:
            uav.move([t,dims,needyPOI])
            printMapGrid(uav.position,list(map(lambda poi : poi.getSection(dims),POIList)))
    
    for uav in UAVList:
        print(list(map(lambda move: move.name,uav.moves)))
        print(uav.valuesArray())
    