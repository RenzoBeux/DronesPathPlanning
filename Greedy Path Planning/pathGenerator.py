from constants import ACTION, DIM, UAVAMOUNT, TIMELENGTH, POIAMOUNT
from random import randint, random, seed
from coordObject import coordObject
from POI import POI
from heuristics.ImoveHeuristic import moveHeuristic
from heuristics.nefesto import heuristic_nefesto

def printMapGrid(dronePos:coordObject, POIPos):
    for aux in range(DIM.y):
        if aux == 0:
            for x in range(DIM.x):
                print('_______', end='')
        print()
        print()
        print('|    ', end='')
        # to print it in right order
        y = DIM.y - aux -1
        for x in range(DIM.x):
            isPOI = [coords for coords in POIPos if (coords.x == x and coords.y == y)] != []
            isDrone = x == dronePos.x and y == dronePos.y
            if(isDrone):
                print('D',end='')
            if(isPOI):
                print('P',end='')
            if(not isPOI and not isDrone):
                print('-',end='')
            # prints a tab
            print('    ',end='')
        print('|', end='')
        print('')
        if aux+1 == DIM.y:
            for x in range(DIM.x):
                print('_______', end='')
        print()





class UAV:

    def __init__(self,dims:coordObject,base:coordObject,heuristic:moveHeuristic):
        self.dims = dims
        self.position = base
        self.free = True
        self.moves = []
        self.target = 0
        self.moveHeuristic = heuristic


    def possibleMoves(self):
        result = []
        moveRight = self.position.x + 1 < self.dims.x
        moveDown = self.position.y -1 >= 0
        moveLeft = self.position.x -1 >= 0
        moveUp = self.position.y +1 < self.dims.y
        result.append(ACTION.STAY)
        if(moveRight):
            result.append(ACTION.RIGHT)
            if(moveDown):
                result.append(ACTION.DIAG_DOWN_RIGHT)
        if(moveDown):
            result.append(ACTION.DOWN)
            if(moveLeft):
                result.append(ACTION.DIAG_DOWN_LEFT)
        if(moveLeft):
            result.append(ACTION.LEFT)
            if(moveUp):
                result.append(ACTION.DIAG_UP_LEFT)
        if(moveUp):
            result.append(ACTION.UP)
            if(moveRight):
                result.append(ACTION.DIAG_UP_RIGHT)
        return result

    def move(self,parameters:list[any]):
        parameters.append(self.position)
        parameters.append(self.possibleMoves())
        move = self.moveHeuristic.getMove(parameters)
        self.shiftPosition(move)
        self.moves.append(move)

    def shiftPosition(self,chosenMove:ACTION):
        if chosenMove == ACTION.STAY:
            pass
        elif chosenMove == ACTION.RIGHT:
            self.position.x = self.position.x + 1
        elif chosenMove == ACTION.DIAG_DOWN_RIGHT:
            self.position.x = self.position.x + 1
            self.position.y = self.position.y - 1
        elif chosenMove == ACTION.DOWN:
            self.position.y = self.position.y - 1
        elif chosenMove == ACTION.DIAG_DOWN_LEFT:
            self.position.y = self.position.y - 1
            self.position.x = self.position.x - 1
        elif chosenMove == ACTION.LEFT:
            self.position.x = self.position.x - 1
        elif chosenMove == ACTION.DIAG_UP_LEFT:
            self.position.x = self.position.x - 1
            self.position.y = self.position.y + 1
        elif chosenMove == ACTION.UP:
            self.position.y = self.position.y + 1
        elif chosenMove == ACTION.DIAG_UP_RIGHT:
            self.position.y = self.position.y + 1
            self.position.x = self.position.x + 1
    
    def valuesArray(self):
        values = []
        for i in range(len(self.moves)):
            values.append(self.moves[i].value)
        return values

def generatePOICoord():
    x = random
    y = random
    return coordObject(x,y)

if __name__ =="__main__":
    # seed(0)
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
        currUAV = UAV(dims,base,heuristic_nefesto())
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
    