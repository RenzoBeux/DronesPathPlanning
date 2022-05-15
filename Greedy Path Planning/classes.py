from random import randint


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
        result.append(0)
        if(moveRight):
            result.append(1)
            if(moveDown):
                result.append(2)
        if(moveDown):
            result.append(3)
            if(moveLeft):
                result.append(4)
        if(moveLeft):
            result.append(5)
            if(moveUp):
                result.append(6)
        if(moveUp):
            result.append(7)
            if(moveRight):
                result.append(8)
        return result

    def setTarget(self,target:POI):
        self.free = False
        self.target = target

    def getMoveTowardsTarget(self,target:POI):
        targetCoords = target.getSection(self.dims)
        results = []
        if self.position.x < targetCoords.x:
            results.append(1)
            if self.position.y < targetCoords.y:
                results.append(2)
        if self.position.y > targetCoords.y:
            results.append(3)
            if self.position.x > targetCoords.x:
                results.append(4)
        if self.position.x > targetCoords.x:
            results.append(5)
            if self.position.y < targetCoords.y:
                results.append(6)
        if self.position.y < targetCoords.y:
            results.append(7)
            if self.position.x < targetCoords.x:
                results.append(8)
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
        if chosenMove == 0:
            pass
        elif chosenMove == 1:
            self.position.x = self.position.x + 1
        elif chosenMove == 2:
            self.position.x = self.position.x + 1
            self.position.y = self.position.y - 1
        elif chosenMove == 3:
            self.position.y = self.position.y - 1
        elif chosenMove == 4:
            self.position.y = self.position.y - 1
            self.position.x = self.position.x - 1
        elif chosenMove == 5:
            self.position.x = self.position.x - 1
        elif chosenMove == 6:
            self.position.x = self.position.x - 1
            self.position.y = self.position.y + 1
        elif chosenMove == 7:
            self.position.y = self.position.y + 1
        elif chosenMove == 8:
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