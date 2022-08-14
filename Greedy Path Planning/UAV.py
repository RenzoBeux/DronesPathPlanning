from POI import POI
from coordObject import coordObject
from heuristics.ImoveHeuristic import moveHeuristic
from constants import *
from utils import xDelta, yDelta, collidesObstacle


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
        """
        THIS HAS TO BE DEPRECATED. TARGETS ARE HEURISTIC LEVEL
        """
        if (self.moveHeuristic.target == None):
            return POI(coordObject(0, 0), 0, -1)
        return self.moveHeuristic.target

    def possibleMoves(self):
        """
        Returns all possile moves. Even those that collide with obstacles
        """
        result:list[ACTION] = []
        # Check for possible moves
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

        return result

    def move(self, parameters: list[any]):
        """
        Either moves according to its heuristic, or it moves towards its charging port
        """
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
            self.battery -= 1
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
        """
        Shifts the position of the drone according to move disregarding everything
        """
        self.position.x += xDelta(chosenMove)
        self.position.y += yDelta(chosenMove)

    def valuesArray(self):
        values = []
        for i in range(len(self.moves)):
            values.append(self.moves[i].value)
        return values

    def moveToCharge(self) -> ACTION:
        """
        Moves to charge fully avoiding obstacles
        """
        targetCoords: coordObject = coordObject(0, 0)
        results: list[ACTION] = []
        position = self.position
        # if im on target the return stay
        if(self.position.x == ORIGIN.x and self.position.y == ORIGIN.y):
            results.append(ACTION.STAY)
            return ACTION.STAY
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

        legalMoves = [value for value in results if value in self.possibleMoves()]
        movesNotObstacles = self.filterObstacles(legalMoves,self.position,self.dims)


        def premise(x): return x in [
            ACTION.DIAG_DOWN_RIGHT, ACTION.DIAG_DOWN_LEFT, ACTION.DIAG_UP_LEFT, ACTION.DIAG_UP_RIGHT]
        # if there is a diagonal move, return it
        if(len(movesNotObstacles) > 0):
            for move in movesNotObstacles:
                if(premise(move)):
                    return move
        # if there is no diagonal move, return the first move
        return movesNotObstacles[0]

    def movesTowardBase(self):
        """
        Returns the number of moves towards ORIGIN
        """
        counter = 0
        auxUAV = UAV(self.dims, coordObject(self.position.x,
                     self.position.y), self.obstaclesRaw, None, -1)
        while (auxUAV.position.x != ORIGIN.x or auxUAV.position.y != ORIGIN.y):
            auxUAV.shiftPosition(auxUAV.moveToCharge())
            counter += 1
        return counter

    def needCharge(self):
        """
        Returns whether the UAV should be moving towards the charging port
        """
        return self.movesTowardBase() >= self.battery

    def filterObstacles(self,moves:list[ACTION],position:coordObject,dims:coordObject) -> list[ACTION]:
        """
        Removes all ACTIONS from a list which would lead to an obstacle
        """
        return list(filter(lambda mov:not collidesObstacle(mov,position,dims),moves))