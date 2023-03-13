from torch import FloatTensor

from collections import Counter
from classes import coordObject, POI, ACTION
from constants import constants
from utils import label_real

def parseFile(fileName) -> list[list[int]]:
  file = open(fileName, 'r')
  res = []
  for line in file:
    res.append(list(map(lambda x: int(x), line.split())))
  return res

def parseMoves(listOfLists: list[list[int]]) -> list[list[ACTION]]:
  res = []
  for line in listOfLists:
    res.append(list(map(lambda x: ACTION(x), line)))
  return res

def populateArea(actions: list[list[ACTION]], areaDims: coordObject) -> tuple[list[list[list[int]]],int]:
  res: list[list[list[int]]] = []
  timeOOB = 0
  for i in range(int(areaDims.x)):
    res.append([])
    for j in range(int(areaDims.y)):
      res[i].append([])
  currentPos: list[coordObject] = []
  for i in range(len(actions)):
    currentPos.append(coordObject(0, 0))
  for i in range(len(actions)):
    res[currentPos[i].x][currentPos[i].y].append(0) # type: ignore
  for i in range(len(actions)):
    for j in range(len(actions[i])):
      chosenMove = actions[i][j]
      if chosenMove == ACTION.RIGHT:
        currentPos[i].x = currentPos[i].x + 1
      elif chosenMove == ACTION.DIAG_DOWN_RIGHT:
        currentPos[i].x = currentPos[i].x + 1
        currentPos[i].y = currentPos[i].y - 1
      elif chosenMove == ACTION.DOWN:
        currentPos[i].y = currentPos[i].y - 1
      elif chosenMove == ACTION.DIAG_DOWN_LEFT:
        currentPos[i].y = currentPos[i].y - 1
        currentPos[i].x = currentPos[i].x - 1
      elif chosenMove == ACTION.LEFT:
        currentPos[i].x = currentPos[i].x - 1
      elif chosenMove == ACTION.DIAG_UP_LEFT:
        currentPos[i].x = currentPos[i].x - 1
        currentPos[i].y = currentPos[i].y + 1
      elif chosenMove == ACTION.UP:
        currentPos[i].y = currentPos[i].y + 1
      elif chosenMove == ACTION.DIAG_UP_RIGHT:
        currentPos[i].y = currentPos[i].y + 1
        currentPos[i].x = currentPos[i].x + 1
      outOfBounds =not (currentPos[i].x in range(int(areaDims.x)) and currentPos[i].y in range(int(areaDims.y)))
      if(outOfBounds):
        timeOOB += 1
      else:
        res[currentPos[i].x][currentPos[i].y].append(j) # type: ignore
  return res, timeOOB


def get_duplicates(array):
  c = Counter(array)
  return {k: v for k, v in c.items() if v > 1}

################################################################################################################################################
########################################################## QUALITY EVALUATOR FUNCTIONS #########################################################
################################################################################################################################################

def evaluateCoverageArea(area: list[list[list[int]]],_, areaDims: coordObject) -> float:
  numberOfSquares = areaDims.x * areaDims.y
  res = numberOfSquares
  for i in range(int(areaDims.x)):
    for j in range(int(areaDims.y)):
      if len(area[i][j]) == 0:
        res = res - 1
  return res / numberOfSquares

def evaluateDronesCollision(area: list[list[list[int]]],actions: list[list[ACTION]], areaDims: coordObject) -> float:
  numberOfDrones = len(actions)
  numberOfTimes = len(actions[0])
  worstCase = numberOfDrones * numberOfTimes
  res = 0
  for i in range(int(areaDims.x)):
    for j in range(int(areaDims.y)):
      if (i == constants.ORIGIN.x and j == constants.ORIGIN.y):
        continue
      duplicates = get_duplicates(area[i][j])
      for k in duplicates:
        res = res + duplicates[k]
  return 1 - (res / worstCase)

def evaluateObstacles(area: list[list[list[int]]],actions: list[list[ACTION]], _) -> float:
  numberOfDrones = len(actions)
  numberOfTimes = len(actions[0])
  worstCase = numberOfDrones * numberOfTimes
  flat_obs = constants.FLAT_OBSTACLES
  timeOnObs = 0
  for obs in flat_obs:
    x = obs.x
    y = obs.y
    timeOnObs += len(area[x][y]) # type: ignore
  return 1 - timeOnObs / worstCase

def evaluatePOICoverage(area: list[list[list[int]]],actions: list[list[ACTION]], areaDims: coordObject) -> float:
  timeSpentNeedy = [0 for _ in constants.POIS]
  lastVisit = [0 for _ in constants.POIS]
  time = len(actions[0])
  pois = [POI(coords, 0, 0) for coords in constants.POIS]
  for t in range(time):
    for i, poi in enumerate(pois):
      coords = poi.getSection(areaDims)
      x = coords.x
      y = coords.y
      if(t in area[x][y]): # type: ignore
        lastVisit[i] = t
      elif(t - lastVisit[i] > constants.POIS_TIMES[i]):
        timeSpentNeedy[i] += 1
  totalTimeSpentNeedy = 0
  for needy in timeSpentNeedy:
    totalTimeSpentNeedy += needy
  maxNeedyTimes = [time-poiTime for poiTime in constants.POIS_TIMES]
  maximumNeediness = 0
  for needy in maxNeedyTimes:
    maximumNeediness += needy
  return 1 - totalTimeSpentNeedy/maximumNeediness

def evaluateDroneUpTime(area: list[list[list[int]]],actions: list[list[ACTION]], areaDims: coordObject) -> float:
  time = len(actions[0])
  dronesUp = 0
  breaked = False
  for t in range(time):
    for i in range(int(areaDims.x)):
      if breaked:
        breaked = False
        break
      for j in range(int(areaDims.y)):
        if (i == constants.ORIGIN.x and j == constants.ORIGIN.y):
          continue
        if(t in area[i][j]):
          dronesUp += 1
          breaked = True
          break
  return dronesUp/time

def evaluate(grid:list[list[ACTION]]):
  gridDimensions = constants.DIM
  area,timeOOB = populateArea(grid,gridDimensions)
  evaluators = {'Coverage':evaluateCoverageArea,'Collision':evaluateDronesCollision,'Obstacles':evaluateObstacles,'POIS':evaluatePOICoverage, 'Uptime': evaluateDroneUpTime}
  evaluateMetric = lambda eval: eval(area,grid,gridDimensions)
  results = {metric:evaluateMetric(eval) for metric, eval in evaluators.items()}
  results['OutOfBound'] = (1 - timeOOB / (len(grid) * len(grid[0]))) ** 8
  accumulator:float = 0
  for v in results.values():
    accumulator += v
  return accumulator/len(results)

def evaluateGAN(generatedList:list[list[int]]):
  """
  Returns:
      Dict[str, float]: Dictionary with the results of the evaluation
      None: If the generated list is invalid
  """
  parsedList = parseMoves(generatedList)
  return evaluate(parsedList)

def evaluator_loss(evals:FloatTensor,loss_fun):
  real = label_real(evals.size)
  return loss_fun(evals,real)