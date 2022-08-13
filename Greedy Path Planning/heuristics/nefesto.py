from heuristics.ImoveHeuristic import moveHeuristic
from coordObject import coordObject
from POI import POI
from constants import *
from utils import collidesObstacle

from random import randint, choices

# moves always to the point


class heuristic_nefesto(moveHeuristic):
    target = None
    free = True
    succProb = 0

    def __init__(self, succProb):
        self.succProb = succProb

    def getMove(self, parameters) -> ACTION:
        # Parse parameters
        time = parameters[0]
        dim = parameters[1]
        needyPOI: list[POI] = parameters[2]
        position: coordObject = parameters[3]
        possibleMoves: list[ACTION] = parameters[4]


        # Deal with target accordingly
        if(self.isOnTarget(position, dim)):
            self.removeTarget(time)
        if(self.isFree() and len(needyPOI) > 0):
            self.setTarget(needyPOI.pop())
        # Chose move accordingly
        if not self.isFree():
            movesTowardsTargetPre: list[ACTION] = self.getMoveTowardsTarget(position, dim)
            movesTowardsTarget = [value for value in movesTowardsTargetPre if value in possibleMoves]

            movesToChoose = [*movesTowardsTarget,*possibleMoves]
            punish = 1-OBS_PUNISH
            probs = [   *[P_SUCC*(1-OBS_PUNISH) if collidesObstacle(mov,position,dim) else P_SUCC for mov in movesTowardsTarget],
                        *[(1-P_SUCC)*(1-OBS_PUNISH) if collidesObstacle(mov,position,dim) else (1-P_SUCC) for mov in possibleMoves]]
            chosenMove = choices(movesToChoose,probs,k=1)[0]
        else:

            randomNumber = randint(0, len(possibleMoves)-1)
            chosenMove = possibleMoves[randomNumber]
        return chosenMove, needyPOI

    def setTarget(self, target: POI):
        self.free = False
        self.target = target

    def removeTarget(self, time):
        self.target.lastVisit = time
        self.target = None
        self.free = True

    def isOnTarget(self, position: coordObject, dim: coordObject):
        if self.target is None:
            return False
        targetCoords = self.target.getSection(dim)
        result: bool = (targetCoords.x == position.x) and (
            targetCoords.y == position.y)
        return result

    def isFree(self) -> bool:
        return self.free

    def getMoveTowardsTarget(self, position: coordObject, dims: coordObject) -> list[ACTION]:
        targetCoords: coordObject = self.target.getSection(dims)
        results: list[ACTION] = []
        # if im on target the return stay
        if(self.isOnTarget(position, dims)):
            results.append(ACTION.STAY)
            return results
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

    # This function removes all ACTIONS from a list which would lead to an obstacle
    def filterObstacles(self,moves:list[ACTION],position:coordObject,dims:coordObject) -> list[ACTION]:
        return list(filter(lambda mov:not collidesObstacle(mov,position,dims),moves))
