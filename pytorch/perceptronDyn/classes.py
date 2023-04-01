from enum import Enum


class coordObject:
  def __init__(self, x: float, y: float):
    self.x = x
    self.y = y

  def copy(self):
    return coordObject(self.x,self.y)

class POI:
  def __init__(self, coords: coordObject, expectedVisitTime: int, id: int):
    # coords is (x,y) pair of numbers in [0..1]
    self.coords = coords
    if (self.coords.x == 1):
        self.coords.x = 0.99
    if (self.coords.y == 1):
        self.coords.y = 0.99
    self.expectedVisitTime = expectedVisitTime
    self.lastVisit = 0
    self.id = id

  def getSection(self, dim: coordObject) -> coordObject:
    percentageOfSectionX = dim.x * self.coords.x
    percentageOfSectionY = dim.y * self.coords.y
    sectionX = int(percentageOfSectionX)
    sectionY = int(percentageOfSectionY)
    result = coordObject(sectionX, sectionY)
    return result

  def markVisited(self, time):
    self.lastVisit = time

class Obstacle:

  def __init__(self, dimsInit: coordObject, dimsEnd: coordObject, id: int):
    self.dimsInit = dimsInit
    self.dimsEnd = dimsEnd
    self.id = id

  def toSections(self, gridDimensions: coordObject) -> list[coordObject]:
    sections = []
    percentageOfSectionInitX = gridDimensions.x * self.dimsInit.x
    percentageOfSectionEndX = gridDimensions.x * self.dimsEnd.x
    percentageOfSectionInitY = gridDimensions.y * self.dimsInit.y
    percentageOfSectionEndY = gridDimensions.y * self.dimsEnd.y
    sectionInitX = int(percentageOfSectionInitX)
    sectionEndX = int(percentageOfSectionEndX)
    sectionInitY = int(percentageOfSectionInitY)
    sectionEndY = int(percentageOfSectionEndY)
    for i in range(sectionInitX, sectionEndX+1):
      for j in range(sectionInitY, sectionEndY+1):
        sections.append(coordObject(i, j))
    return sections

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