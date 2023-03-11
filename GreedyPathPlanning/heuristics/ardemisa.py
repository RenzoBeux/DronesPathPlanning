from GreedyPathPlanning.POI import POI
from GreedyPathPlanning.constants import ACTION
from GreedyPathPlanning.coordObject import coordObject
from heuristics.ImoveHeuristic import moveHeuristic

class heuristic_ardemisa(moveHeuristic):
  target = None
  free = True
  succProb = 0

  def getMove(self, parameters: list) -> ACTION:
    time = parameters[0]
    dim = parameters[1]
    needyPOI: list[POI] = parameters[2]
    position: coordObject = parameters[3]
    possibleMoves: list[ACTION] = parameters[4]

    if len(needyPOI) > 0:
        self.setTarget(needyPOI[0])
        
    
    return ACTION.DIAG_DOWN_LEFT
  
  def setTarget(self, target: POI):
      self.free = False
      self.target = target

  def removeTarget(self, time):
    self.free = True
    if self.target == None:
      return  
    self.target.lastVisit = time
    self.target = None

  def isOnTarget(self, position: coordObject, dim: coordObject):
      if self.target is None:
          return False
      targetCoords = self.target.getSection(dim)
      result: bool = (targetCoords.x == position.x) and (
          targetCoords.y == position.y)
      return result

  def getMoveTowardsTarget(self, position: coordObject, dims: coordObject) -> list[ACTION]:
    if self.target == None:
      raise Exception('No target set for getMoveTowardsTarget')
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