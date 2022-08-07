from coordObject import coordObject
from constants import ACTION, BIGDIM, DIM, ORIGIN, OBSTACLES
from utils import readFileAction
from math import floor
from routeDrawer import drawRouteAlt

def converter1(originalDim:coordObject,targetDim:coordObject,moves:list[ACTION]):
    """
    This resizer assumes the dimensions of originalDim are a strict multiple of the dimensions of target dim
    The multiple each dimension is of the other must be the same for both x and y
    A move is only recorded in the case the UAV crosses the threshold from a quadrant in the bigDimensions
    """
    ratio = originalDim.x / targetDim.x
    targCoord = coordObject(ORIGIN.x,ORIGIN.y)
    origCoord = coordObject(ORIGIN.x,ORIGIN.y)
    time = 0
    result = []
    for move in moves:
        origCoord.x += xDelta(move)
        origCoord.y += yDelta(move)
        time += 1
        if time % ratio == 0:
            newXCoord = floor(origCoord.x / ratio)
            newYCoord = floor(origCoord.y / ratio)
            result.append(deltaToACTION(newXCoord - targCoord.x,newYCoord - targCoord.y))
            targCoord.x = newXCoord
            targCoord.y = newYCoord
    return result


def xDelta(move:ACTION):
    positives = [ACTION.DIAG_DOWN_RIGHT,ACTION.RIGHT,ACTION.DIAG_UP_RIGHT]
    negatives = [ACTION.DIAG_DOWN_LEFT,ACTION.LEFT, ACTION.DIAG_UP_LEFT]
    if move in positives:
        return 1
    elif move in negatives:
        return -1
    else:
        return 0

def yDelta(move:ACTION):
    positives = [ACTION.DIAG_UP_RIGHT,ACTION.DIAG_UP_LEFT,ACTION.UP]
    negatives = [ACTION.DIAG_DOWN_RIGHT,ACTION.DIAG_DOWN_LEFT, ACTION.DOWN]
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
                

def resizeRoute(name:str) -> list[list[ACTION]]:
    moves = readFileAction(name)
    return list(map(lambda r:converter1(BIGDIM,DIM,r),moves))

if __name__ == "__main__":
    routes = resizeRoute('./output/70/1.txt')
    oldRoutes = readFileAction('./output/70/1.txt')
    drawRouteAlt(BIGDIM,[],ORIGIN,OBSTACLES,oldRoutes)
    drawRouteAlt(DIM,[],ORIGIN,OBSTACLES,routes)