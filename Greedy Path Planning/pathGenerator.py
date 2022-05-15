from constants import *
from classes import *
from random import random, seed

def generatePOICoord():
    x = random
    y = random
    return coordObject(x,y)

if __name__ =="__main__":
    seed(1)
    base = coordObject(0,0)
    dims = DIM
    amountOfUAV = UAVAMOUNT
    POIPosition = [coordObject(1,1)]
    POITimes = [10]
    POIList:list[POI] = []
    UAVList:list[UAV] = []
    needyPOI:list[POI] = []
    for i in range(POIAMOUNT):
        currPOI = POI(POIPosition[i],POITimes[i])
        POIList.append(currPOI)
        needyPOI.append(currPOI)
    for i in range(UAVAMOUNT):
        currUAV = UAV(dims,base)
        UAVList.append(currUAV)
    for t in range(TIMELENGTH):
        print(UAVList[0].position.x,' ',UAVList[0].position.y)
        for uav in UAVList:
            if uav.isOnTarget():
                uav.removeTarget()
        for poi in needyPOI:
            for uav in UAVList:
                if uav.isFree():
                    uav.setTarget(poi)
        for uav in UAVList:
            uav.move()
    
    for uav in UAVList:
        print(uav.valuesArray())
    