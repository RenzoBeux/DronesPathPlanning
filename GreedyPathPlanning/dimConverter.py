from coordObject import coordObject
from constants import ACTION, BIGDIM, DIM, ORIGIN, OBSTACLES
from utils import readFileAction, xDelta, yDelta, deltaToACTION
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

def resizeRoute(name:str) -> list[list[ACTION]]:
    moves = readFileAction(name)
    return list(map(lambda r:converter1(BIGDIM,DIM,r),moves))

if __name__ == "__main__":
    routes = resizeRoute('./output/70/1.txt')
    oldRoutes = readFileAction('./output/70/1.txt')
    drawRouteAlt(BIGDIM,[],ORIGIN,OBSTACLES,oldRoutes)
    drawRouteAlt(DIM,[],ORIGIN,OBSTACLES,routes)