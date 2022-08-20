from constants import ACTION, DIM, OBSTACLES,POIS,POIS_TIMES
from coordObject import coordObject
from POI import POI

def readFileAction(fileName:str)-> list[list[ACTION]]:
    """
    Reads a file and interprets it as a list of sequences of ACTIONs
    """
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
    result = []
    for line in lines:
        line = line.replace('\n', '')
        result.append(list(map(lambda x: ACTION(int(x)), line.split(' '))))
    return result

def flatten_obstacles(areaDims:coordObject)->list[coordObject]:
    """
    Returns a list of all of the coordinates which are considered occupied by obstacles
    """
    obstaclesBySections:list[list[coordObject]] = list(map(lambda obs:obs.toSections(areaDims),OBSTACLES))
    flat_obs:list[coordObject] = []
    # Suboptimal as all hell
    for sectionList in obstaclesBySections:
        for section in sectionList:
            isAccounted = False
            for alreadyAccounted in flat_obs:
                if(alreadyAccounted.x == section.x and alreadyAccounted.y == section.y):
                    isAccounted = True
                    break
            if(not isAccounted):
                flat_obs.append(section)
    return flat_obs

def collidesObstacle(action:ACTION,position:coordObject,dims=DIM)->bool:
    """
    Returns whether an action would lead to a collission with an obstacle
    """
    obstacles = flatten_obstacles(dims)
    newX = position.x + xDelta(action)
    newY = position.y + yDelta(action)
    for obs in obstacles:
        if (obs.x == newX and obs.y == newY):
            return True
    return False

def xDelta(move: ACTION):
    """
    Calculates the shift an ACTION produces in the X axis
    """
    positives = [ACTION.DIAG_DOWN_RIGHT, ACTION.RIGHT, ACTION.DIAG_UP_RIGHT]
    negatives = [ACTION.DIAG_DOWN_LEFT, ACTION.LEFT, ACTION.DIAG_UP_LEFT]
    if move in positives:
        return 1
    elif move in negatives:
        return -1
    else:
        return 0

def yDelta(move: ACTION):
    """
    Calculates the shift an ACTION produces in the Y axis
    """
    positives = [ACTION.DIAG_UP_RIGHT, ACTION.DIAG_UP_LEFT, ACTION.UP]
    negatives = [ACTION.DIAG_DOWN_RIGHT, ACTION.DIAG_DOWN_LEFT, ACTION.DOWN]
    if move in positives:
        return 1
    elif move in negatives:
        return -1
    else:
        return 0

def deltaToACTION(xDelta:int,yDelta:int)->ACTION:
    """
    Given the delta an action makes to the x and y coordinates returns which action it is
    """
    if xDelta > 0:
        if yDelta > 0:
            return ACTION.DIAG_UP_RIGHT
        elif yDelta < 0:
            return ACTION.DIAG_DOWN_RIGHT
        else:
            return ACTION.RIGHT
    elif xDelta < 0:
        if yDelta > 0:
            return ACTION.DIAG_UP_LEFT
        elif yDelta < 0:
            return ACTION.DIAG_DOWN_LEFT
        else:
            return ACTION.LEFT

    if yDelta > 0:
        return ACTION.UP
    elif yDelta < 0:
        return ACTION.DOWN
    else:
        return ACTION.STAY

def getListOfPois()->list[POI]:
    """
    Returns a list of POI objects, for all of the POIs in the scenario
    """
    return [POI(coord,POIS_TIMES[i],i) for i, coord in enumerate(POIS)]