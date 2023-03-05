from POI import POI
from constants import ACTION
from utils import getMoveFromTo
from coordObject import coordObject
from heuristics.ImoveHeuristic import moveHeuristic
from random import choice,randint


class heuristic_ardemisa(moveHeuristic):
  target = None

  def isOnTarget(self, position: coordObject, dim: coordObject):
    if self.target is None:
      return False
    targetCoords = self.target.getSection(dim)
    result: bool = (targetCoords.x == position.x) and (
      targetCoords.y == position.y)
    return result

  def getMove(self, parameters: list) -> tuple[ACTION, list[POI]]:
    time = parameters[0]
    dim = parameters[1]
    needyPOI: list[POI] = parameters[2]
    position: coordObject = parameters[3]
    possibleMoves: list[ACTION] = parameters[4]
    movs = possibleMoves

    if self.target != None or len(needyPOI) > 0:
      if self.target == None:
        poiIndex = randint(0,len(needyPOI)-1)
        self.target = needyPOI.pop(poiIndex)
      if self.isOnTarget(position,dim):
        self.target.markVisited(time)
        self.target = None
      else:
        movs = getMoveFromTo(position,self.target.getSection(dim))
    
    return choice(movs),needyPOI