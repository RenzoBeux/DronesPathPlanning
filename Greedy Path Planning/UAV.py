from POI import POI
from coordObject import coordObject
from heuristics.ImoveHeuristic import moveHeuristic
from constants import *


class UAV:

    def __init__(self, dims: coordObject, base: coordObject, obstacles: list[Obstacle], heuristic: moveHeuristic, id: int):
        self.dims = dims
        self.position = base
        self.free = True
        self.moves = []
        self.obstacles: set[coordObject] = set()
        for obstacle in obstacles:
            for object in obstacle.toSections(dims):
                self.obstacles.add(object)
        self.obstaclesRaw = obstacles
        self.moveHeuristic = heuristic
        self.battery = BATTERY_CAPACITY
        self.charging = False
        self.chargingTime = TIME_TO_CHARGE
        self.id = id

    def getTarget(self):
        if (self.moveHeuristic.target == None):
            return POI(coordObject(0, 0), 0, -1)
        return self.moveHeuristic.target

    def possibleMoves(self):
        result = []
        moveRight = self.position.x + 1 < self.dims.x
        moveDown = self.position.y - 1 >= 0
        moveLeft = self.position.x - 1 >= 0
        moveUp = self.position.y + 1 < self.dims.y
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

        # Now we have to remove those actions that lead to an obstacle
        for obstacle in self.obstacles:
            for move in result:
                if(move == ACTION.STAY):
                    continue
                if(move == ACTION.RIGHT):
                    if(self.position.x + 1 == obstacle.x and self.position.y == obstacle.y):
                        result.remove(ACTION.RIGHT)
                if(move == ACTION.DIAG_DOWN_RIGHT):
                    if(self.position.x + 1 == obstacle.x and self.position.y - 1 == obstacle.y):
                        result.remove(ACTION.DIAG_DOWN_RIGHT)
                if(move == ACTION.DOWN):
                    if(self.position.x == obstacle.x and self.position.y - 1 == obstacle.y):
                        result.remove(ACTION.DOWN)
                if(move == ACTION.DIAG_DOWN_LEFT):
                    if(self.position.x - 1 == obstacle.x and self.position.y - 1 == obstacle.y):
                        result.remove(ACTION.DIAG_DOWN_LEFT)
                if(move == ACTION.LEFT):
                    if(self.position.x - 1 == obstacle.x and self.position.y == obstacle.y):
                        result.remove(ACTION.LEFT)
                if(move == ACTION.DIAG_UP_LEFT):
                    if(self.position.x - 1 == obstacle.x and self.position.y + 1 == obstacle.y):
                        result.remove(ACTION.DIAG_UP_LEFT)
                if(move == ACTION.UP):
                    if(self.position.x == obstacle.x and self.position.y + 1 == obstacle.y):
                        result.remove(ACTION.UP)
                if(move == ACTION.DIAG_UP_RIGHT):
                    if(self.position.x + 1 == obstacle.x and self.position.y + 1 == obstacle.y):
                        result.remove(ACTION.DIAG_UP_RIGHT)
        return result

    def move(self, parameters: list[any]):
        if (self.charging):
            self.chargingTime -= 1
            if (self.chargingTime == 0):
                self.charging = False
                self.battery = BATTERY_CAPACITY
                return parameters[2]  # returneo el needy poi como me vino
        if (self.needCharge()):
            move = self.moveToCharge()
            if (move == ACTION.STAY):
                self.charging = True
            self.shiftPosition(move)
            self.moves.append(move)
            return parameters[2]  # returneo el needy poi como me vino
        else:
            self.battery -= 1
            parameters.append(self.position)
            parameters.append(self.possibleMoves())
            move, needyPOI = self.moveHeuristic.getMove(parameters)
            self.shiftPosition(move)
            self.moves.append(move)
            return needyPOI

    def shiftPosition(self, chosenMove: ACTION):
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

    def moveToCharge(self) -> ACTION:
        # gets the most direct move towards cordObject(0,0)
        if (self.position.x == 0 and self.position.y == 0):
            return ACTION.STAY
        if (self.position.x == 0):
            if (self.position.y > 0):
                return ACTION.DOWN
        if (self.position.y == 0):
            if (self.position.x > 0):
                return ACTION.LEFT
        if (self.position.x > 0 and self.position.y > 0):
            return ACTION.DIAG_DOWN_LEFT

        return ACTION.STAY

# This function returns the number of moves towards cordObject(0,0)
    def movesTowardBase(self):
        counter = 0
        auxUAV = UAV(self.dims, coordObject(self.position.x,
                     self.position.y), self.obstaclesRaw, None, -1)
        while (auxUAV.position.x != 0 or auxUAV.position.y != 0):
            auxUAV.shiftPosition(auxUAV.moveToCharge())
            counter += 1
        return counter

    def needCharge(self):
        return self.movesTowardBase() >= self.battery
