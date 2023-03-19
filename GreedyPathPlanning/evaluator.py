# this function parses the txt file and returns a list of lists
from collections import Counter
from constants import ORIGIN, POIS, POIS_TIMES, ACTION, coordObject, DIM, colors, metrics
from utils import flatten_obstacles
from POI import POI
import matplotlib.pyplot as plt


def parseFile(fileName) -> list[list[int]]:
    file = open(fileName, 'r')
    res = []
    for line in file:
        res.append(list(map(lambda x: int(x), line.split())))
    return res

# given a list of lists of ints, returns a list of ACTIONS


def parseMoves(listOfLists: list[list[int]]) -> list[ACTION]:
    res = []
    for line in listOfLists:
        res.append(list(map(lambda x: ACTION(x), line)))
    return res

# this will return a matrix of lists of ints where each int is the time a drone passed by that square


def populateArea(actions: list[list[ACTION]], areaDims: coordObject) -> tuple[list[list[list[int]]],int]:
    res: list[list[list[int]]] = []
    currentPos: list[coordObject] = []
    oob_pen:list[float] = []
    total_time = len(actions[0])
    time_oob = 0
    num_uavs = len(actions)
    for i in range(areaDims.x):
        res.append([])
        for j in range(areaDims.y):
            res[i].append([])

    for i in range(num_uavs):
        currentPos.append(coordObject(0, 0))
        oob_pen.append(0)
        res[currentPos[i].x][currentPos[i].y].append(0)
    for i in range(num_uavs):
        for j in range(len(actions[i])):
            oob_penalize = 0
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
            how_far_x = min(currentPos[i].x,areaDims.x - currentPos[i].x - 1)
            how_far_y = min(currentPos[i].y,areaDims.y - currentPos[i].y - 1)
            if how_far_x < 0 or how_far_y < 0:
              time_oob += 1
              oob_penalize += min(how_far_x,0)
              oob_penalize += min(how_far_y,0)
              oob_pen[i] += oob_penalize
            else:
              res[currentPos[i].x][currentPos[i].y].append(j)
    max_pen = 0
    for pen in oob_pen:
      if pen < max_pen:
        max_pen = pen
    max_pen = -max_pen/((total_time+1)*total_time)
    return res, 1-max_pen, 1-time_oob/(num_uavs*total_time)


def get_duplicates(array):
    c = Counter(array)
    return {k: v for k, v in c.items() if v > 1}

################################################################################################################################################
########################################################## QUALITY EVALUATOR FUNCTIONS #########################################################
################################################################################################################################################

# This function evaluates the coverage of the area
def evaluateCoverageArea(_: list[list[ACTION]], areaDims: coordObject,area: list[list[list[int]]]) -> float:
    numberOfSquares = areaDims.x * areaDims.y
    res = numberOfSquares
    for i in range(areaDims.x):
        for j in range(areaDims.y):
            if len(area[i][j]) == 0:
                res = res - 1
    return res / numberOfSquares

# This function will reward if drones don't share the same square at the same time
def evaluateDronesCollision(actions: list[list[ACTION]], areaDims: coordObject,area: list[list[list[int]]]) -> float:
    numberOfDrones = len(actions)
    numberOfTimes = len(actions[0])
    worstCase = numberOfDrones * numberOfTimes  # all time moves together
    res = 0
    for i in range(areaDims.x):
        for j in range(areaDims.y):
            # find the repeted times in the list
            # we dont want to take into account the base
            if (i == ORIGIN.x and j == ORIGIN.y):
                continue
            duplicates = get_duplicates(area[i][j])
            for k in duplicates:
                res = res + duplicates[k]

    return 1 - (res / worstCase)

# This function will reward drones for not flying over obstacles
def evaluateObstacles(actions: list[list[ACTION]], areaDims: coordObject,area: list[list[list[int]]]) -> float:
    numberOfDrones = len(actions)
    numberOfTimes = len(actions[0])
    worstCase = numberOfDrones * numberOfTimes
    flat_obs = flatten_obstacles(areaDims)

    timeOnObs = 0
    for obs in flat_obs:
        x = obs.x
        y = obs.y
        timeOnObs += len(area[x][y])

    return 1 - timeOnObs / worstCase

def evaluatePOICoverage(actions: list[list[ACTION]], areaDims: coordObject,area: list[list[list[int]]]) -> float:
    timeSpentNeedy = [0 for _ in POIS]
    lastVisit = [0 for _ in POIS]
    time = len(actions[0])
    pois = [POI(coords, 0, 0) for coords in POIS]
    for t in range(time):
        for i, poi in enumerate(pois):
            coords = poi.getSection(areaDims)
            x = coords.x
            y = coords.y
            if(t in area[x][y]):
                lastVisit[i] = t
            elif(t - lastVisit[i] > POIS_TIMES[i]):
                timeSpentNeedy[i] += 1

    totalTimeSpentNeedy = 0
    for needy in timeSpentNeedy:
        totalTimeSpentNeedy += needy

    maxNeedyTimes = [time-poiTime for poiTime in POIS_TIMES]
    maximumNeediness = 0
    for needy in maxNeedyTimes:
        maximumNeediness += needy

    return 1 - totalTimeSpentNeedy/maximumNeediness

# This function will give  the best score if for all times there at least one drone outside base
def evaluateDroneUpTime(actions: list[list[ACTION]], areaDims: coordObject,area:list[list[list[int]]]) -> float:
    time = len(actions[0])
    dronesUp = 0
    breaked = False
    for t in range(time):
        for i in range(areaDims.x):
            if breaked:
                breaked = False
                break
            for j in range(areaDims.y):
                # we dont want to take into account the base
                if (i == ORIGIN.x and j == ORIGIN.y):
                    continue
                if(t in area[i][j]):
                    dronesUp += 1
                    breaked = True
                    break
    return dronesUp/time

def evaluate(grid:list[list[ACTION]]):
    gridDimensions = DIM
    area,oob_dist,oob_time = populateArea(grid,gridDimensions)
    evaluators = {'Coverage':evaluateCoverageArea,'Collision':evaluateDronesCollision,'Obstacles':evaluateObstacles,'POIS':evaluatePOICoverage, 'Uptime': evaluateDroneUpTime}
    evaluateMetric = lambda eval: eval(grid,gridDimensions,area)
    results = {metric:evaluateMetric(eval) for metric, eval in evaluators.items()}
    results['OutOfBound'] = (oob_dist + oob_time)/ 2
    accumulator = 0
    for v in results.values():
        accumulator += v
    # return accumulator/len(results)
    return results['OutOfBound']

def evaluateGAN(generatedList:list[list[int]]) -> dict[str,float] or None:
    """
    Returns:
        Dict[str, float]: Dictionary with the results of the evaluation
        None: If the generated list is invalid
    """
    parsedList = parseMoves(generatedList)
    return evaluate(parsedList)

def evaluateFile(file:str):
    moves = parseFile(file)
    return evaluateGAN(moves)


def evaluateOutputs():
    finalGraph = {metric:[] for metric in metrics}
    for probToGoTarget in range(70,100):
        partialGraph = {metric:0 for metric in metrics}
        for i in range(1,10):
            fileToParse = 'output/'+str(probToGoTarget)+'/'+str(i)+'.txt'
            list = parseFile(fileToParse)
            listOfRoutes = parseMoves(list)
            evalResults = evaluate(listOfRoutes)
            partialGraph = {k:v+partialGraph[k] for k,v in evalResults.items()}
        finalGraph = {k:finalGraph[k] + [partialGraph[k]/9] for k in partialGraph.keys()}

    bar_width = 0.2
    plt.ylabel('Scores')
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    index = 0
    for v in finalGraph.values():
        X = [i + index * bar_width for i in range(70,100)]
        plt.bar(X, v , color = colors[index], width = bar_width)
        index += 1
    plt.show()
