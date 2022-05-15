from random import randint
from enum import Enum

class ACTION(Enum):
    STAY = 0
    RIGHT = 1
    DIAG_DOWN_RIGHT = 2
    DOWN = 3
    DIAG_DOWN_LEFT = 4
    LEFT = 5
    DIAG_UP_LEFT = 6
    UP = 7
    DIAG_UP_RIGHT = 8 



class coordObject:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class POI:
    def __init__(self,coords:coordObject,expectedVisitTime:int):
        # coords is (x,y) pair of numbers in [0..1]
        self.coords = coords
        self.expectedVisitTime = expectedVisitTime
        self.lastVisit = 0

    def getSection(self,dim:coordObject):
        percentageOfSectionX = dim.x / self.coords.y
        percentageOfSectionY = dim.y / self.coords.y
        sectionX = int(self.coords.x / percentageOfSectionX)
        sectionY = int(self.coords.y / percentageOfSectionY)
        result = coordObject(sectionX,sectionY)
        return result

    def markVisited(self,time):
        self.lastVisit = time

class UAV:

    def __init__(self,dims:coordObject,base:coordObject):
        self.dims = dims
        self.position = base
        self.free = True
        self.moves = []
        self.target = 0

    def possibleMoves(self):
        result = []
        moveRight = self.position.y + 1 <= self.dims.x
        moveDown = self.position.y -1 >= 0
        moveLeft = self.position.x -1 >= 0
        moveUp = self.position.y +1 <= self.dims.y
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

    def setTarget(self,target:POI):
        self.free = False
        self.target = target

    def getMoveTowardsTarget(self,target:POI):
        targetCoords = target.getSection(self.dims)
        results = []
        if self.position.x < targetCoords.x:
            results.append(ACTION.RIGHT)
            if self.position.y < targetCoords.y:
                results.append(ACTION.DIAG_DOWN_RIGHT)
        if self.position.y > targetCoords.y:
            results.append(ACTION.DOWN)
            if self.position.x > targetCoords.x:
                results.append(ACTION.DIAG_DOWN_LEFT)
        if self.position.x > targetCoords.x:
            results.append(ACTION.LEFT)
            if self.position.y < targetCoords.y:
                results.append(ACTION.DIAG_UP_LEFT)
        if self.position.y < targetCoords.y:
            results.append(ACTION.UP)
            if self.position.x < targetCoords.x:
                results.append(ACTION.DIAG_UP_RIGHT)
        return results

    def move(self):
        possibleMoves = self.possibleMoves()
        if self.target != 0:
            movesTowardsTarget = self.getMoveTowardsTarget(self.target)
            probMoves = [*possibleMoves,*movesTowardsTarget]
            randomNumber = randint(0,len(probMoves))
            chosenMove = probMoves[randomNumber]
            self.shiftPosition(chosenMove)
            self.moves.append(chosenMove)
            pass
        else:
            randomNumber = randint(0,len(possibleMoves))
            chosenMove = possibleMoves[randomNumber]
            self.shiftPosition(chosenMove)
            self.moves.append(chosenMove)

    def shiftPosition(self,chosenMove):
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

    def isFree(self):
        return self.free

    def removeTarget(self):
        self.target = 0
        self.free = True

    def isOnTarget(self):
        if self.target == 0:
            return False
        return (self.position.x == self.target.getSection(self.dims).x) and (self.position.y == self.target.getSection(self.dims).y)
    
    def valuesArray(self):
        values = []
        for i in range(len(self.moves)):
            values.append(self.moves[i].value)
        return values