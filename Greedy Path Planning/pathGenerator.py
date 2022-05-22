from constants import ACTION
from random import randint, random, seed

class coordObject:
    def __init__(self,x,y):
        self.x = x
        self.y = y

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

DIM = coordObject(3,3)
UAVAMOUNT = 1
TIMELENGTH = 10
POIAMOUNT = 1

class POI:
    def __init__(self,coords:coordObject,expectedVisitTime:int):
        # coords is (x,y) pair of numbers in [0..1]
        self.coords = coords
        self.expectedVisitTime = expectedVisitTime
        self.lastVisit = 0

    def getSection(self,dim:coordObject)->coordObject:
        percentageOfSectionX = dim.x * self.coords.x
        percentageOfSectionY = dim.y * self.coords.y
        sectionX = int(percentageOfSectionX)
        sectionY = int(percentageOfSectionY)
        result = coordObject(sectionX,sectionY)
        return result

    def markVisited(self,time):
        self.lastVisit = time

class moveHeuristic:
    def getMove(self,parameters:list)->ACTION:
        pass

class heuristic01(moveHeuristic):
    target = 0
    free = True

    def getMove(self,parameters)->ACTION:
        # Parse parameters
        time = parameters[0]
        dim = parameters[1]
        needyPOI:list[POI] = parameters[2]
        position = parameters[3]
        possibleMoves:list[ACTION] = parameters[4]
        # Deal with target accordingly
        if(self.isOnTarget(position,dim)):
            self.removeTarget(time)
        if(self.isFree() and len(needyPOI) > 0):
            self.setTarget(needyPOI.pop())
        # Chose move accordingly
        if not self.isFree():
            movesTowardsTarget:list[ACTION] = self.getMoveTowardsTarget(self.target.getSection(dim),dim)
            probMoves = [*possibleMoves,*movesTowardsTarget]
            randomNumber = randint(0,len(probMoves)-1)
            chosenMove = probMoves[randomNumber]
        else:
            randomNumber = randint(0,len(possibleMoves)-1)
            chosenMove = possibleMoves[randomNumber]
        return chosenMove

    def setTarget(self,target:POI):
        self.free = False
        self.target = target
    
    def removeTarget(self,time):
        self.target.lastVisit = time
        self.target = 0
        self.free = True

    def isOnTarget(self,position:coordObject,dim:coordObject):
        if self.target == 0:
            return False
        targetCoords = self.target.getSection(dim)
        result:bool = (targetCoords.x == position.x) and (targetCoords.y == position.y)
        return result

    def isFree(self)->bool:
        return self.free

    def getMoveTowardsTarget(self,position:coordObject,dims:coordObject)->list[ACTION]:
        targetCoords:coordObject = self.target.getSection(dims)
        results:list[ACTION] = []
        if position.x < targetCoords.x:
            results.append(ACTION.RIGHT)
            if position.y > targetCoords.y:
                results.append(ACTION.DIAG_DOWN_RIGHT)
        if position.y > targetCoords.y:
            results.append(ACTION.DOWN)
            if position.x > targetCoords.x:
                results.append(ACTION.DIAG_DOWN_LEFT)
        if position.x > targetCoords.x:
            results.append(ACTION.LEFT)
            if position.y < targetCoords.y:
                results.append(ACTION.DIAG_UP_LEFT)
        if position.y < targetCoords.y:
            results.append(ACTION.UP)
            if position.x < targetCoords.x:
                results.append(ACTION.DIAG_UP_RIGHT)
        return results

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
        currUAV = UAV(dims,base,heuristic01())
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
    