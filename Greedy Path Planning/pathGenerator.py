from constants import ACTION, DIM, UAVAMOUNT, TIMELENGTH, POIAMOUNT
from random import randint, random, seed
from coordObject import coordObject
from POI import POI
from UAV import UAV
from heuristics.ImoveHeuristic import moveHeuristic
from heuristics.nefesto import heuristic_nefesto


def printMapGrid(dronePos: coordObject, POIPos):
    for aux in range(DIM.y):
        if aux == 0:
            for x in range(DIM.x):
                print('_______', end='')
        print()
        print()
        print('|    ', end='')
        # to print it in right order
        y = DIM.y - aux - 1
        for x in range(DIM.x):
            isPOI = [coords for coords in POIPos if (
                coords.x == x and coords.y == y)] != []
            isDrone = x == dronePos.x and y == dronePos.y
            if(isDrone):
                print('D', end='')
            if(isPOI):
                print('P', end='')
            if(not isPOI and not isDrone):
                print('-', end='')
            # prints a tab
            print('    ', end='')
        print('|', end='')
        print('')
        if aux+1 == DIM.y:
            for x in range(DIM.x):
                print('_______', end='')
        print()


def generatePOICoord():
    x = random
    y = random
    return coordObject(x, y)


if __name__ == "__main__":
    # seed(0)
    base = coordObject(0, 0)
    dims = DIM
    amountOfUAV = UAVAMOUNT
    POIPosition = [coordObject(0.5, 0.5)]
    POITimes = [10]
    POIList: list[POI] = []
    UAVList: list[UAV] = []
    needyPOI: list[POI] = []
    printMapGrid(base, POIPosition)
    # POI and UAV creation
    for i in range(POIAMOUNT):
        currPOI = POI(POIPosition[i], POITimes[i])
        POIList.append(currPOI)
        needyPOI.append(currPOI)
    for i in range(UAVAMOUNT):
        currUAV = UAV(dims, base, heuristic_nefesto())
        UAVList.append(currUAV)
    # Creation of the routes
    for t in range(TIMELENGTH):
        print(UAVList[0].position.x, ' ', UAVList[0].position.y)
        for poi in POIList:
            if (not(poi in needyPOI) and (t - poi.lastVisit > poi.expectedVisitTime)):
                needyPOI.append()
        for uav in UAVList:
            uav.move([t, dims, needyPOI])
            printMapGrid(uav.position, list(
                map(lambda poi: poi.getSection(dims), POIList)))

    for uav in UAVList:
        print(list(map(lambda move: move.name, uav.moves)))
        print(uav.valuesArray())
