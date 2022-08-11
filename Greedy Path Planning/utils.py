from constants import ACTION, DIM, OBSTACLES
from coordObject import coordObject


# def printMapGrid(drones: list[UAV], POIPos: list[coordObject], obstacles: list[coordObject]):
#     for aux in range(DIM.y):
#         if aux == 0:
#             for x in range(DIM.x):
#                 print('_______', end='')
#         print()
#         print()
#         print('|    ', end='')
#         # to print it in right order
#         y = DIM.y - aux - 1
#         for x in range(DIM.x):
#             isPOI = [coords for coords in POIPos if (
#                 coords.x == x and coords.y == y)] != []
#             isObstacle = [coords for coords in obstacles if (
#                 coords.x == x and coords.y == y)] != []
#             filtered = list(filter(
#                 lambda drone: x == drone.position.x and y == drone.position.y, drones))
#             isDrone = list(filtered) != []
#             if(isDrone):
#                 for d in filtered:
#                     print('D'+str(d.id), end='')
#             if(isPOI):
#                 print('P', end='')
#             if(isObstacle):
#                 print('O', end='')
#             if(not isPOI and not isDrone and not isObstacle):
#                 print('-', end='')
#             # prints a tab
#             print('    ', end='')
#         print('|', end='')
#         print('')
#         if aux+1 == DIM.y:
#             for x in range(DIM.x):
#                 print('_______', end='')
#         print()


def readFileAction(fileName):
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

def collidesObstacle(action:ACTION,position:coordObject,dims=DIM):
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