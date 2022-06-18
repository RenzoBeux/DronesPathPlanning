from coordObject import coordObject
from math import gcd
from constants import ACTION, BIGDIM, DIM
from utils import readFileAction

def converter1(originalDim:coordObject,targetDim:coordObject,moves:list[ACTION]):
    """
    :param originalDim: the original dimension of the board
    :param targetDim: the target dimension of the board
    :param moves: the list of moves to be converted
    :return: the converted list of moves
    Resizes de original set of moves to a the target dimensions
    The time of the converted route is determined by the ratio of the areas of the dimensions
    """
    xGCD = gcd(originalDim.x,targetDim.x)
    yGCD = gcd(originalDim.y,targetDim.y)
    xScale = (int(originalDim.x / xGCD) , int(targetDim.x / xGCD)) # 5:2
    yScale = (int(originalDim.y / yGCD) , int(targetDim.y / yGCD))
    originalArea = originalDim.x * originalDim.y 
    targetArea = targetDim.x * targetDim.y
    tScale = (int(originalArea / targetArea ),1)
    xMovement = 0
    yMovement = 0
    t = 0
    result = []
    # This currently prefers diag down over the other moves
    for move in moves:
        xMovement +=xDelta(move)
        yMovement +=yDelta(move)
        t+=1
        if (t % tScale[0]) == 0:
            if xMovement >= xScale[0]:
                if yMovement >= yScale[0]:
                    for _ in range(xScale[1]):
                        result.append(ACTION.DIAG_UP_RIGHT)
                    xMovement -= xScale[0]
                    yMovement -= yScale[0]
                elif yMovement <= -yScale[0]:
                    for _ in range(xScale[1]):
                        result.append(ACTION.DIAG_DOWN_RIGHT)
                    xMovement -= xScale[0]
                    yMovement += yScale[0]
                else:
                    for _ in range(xScale[1]):
                        result.append(ACTION.RIGHT)
                        xMovement -= xScale[0]
            elif xMovement <= -xScale[0]:
                if yMovement >= yScale[0]:
                    for _ in range(xScale[1]):
                        result.append(ACTION.DIAG_UP_LEFT)
                    xMovement += xScale[0]
                    yMovement -= yScale[0]
                elif yMovement <= -yScale[0]:
                    for _ in range(xScale[1]):
                        result.append(ACTION.DIAG_DOWN_LEFT)
                    xMovement += xScale[0]
                    yMovement += yScale[0]
                else:
                    for _ in range(xScale[1]):
                        result.append(ACTION.LEFT)
                        xMovement += xScale[0]
            elif yMovement >= yScale[0]:
                for _ in range(yScale[1]):
                    result.append(ACTION.UP)
                yMovement -= yScale[0]
            elif yMovement <= -yScale[0]:
                for _ in range(yScale[1]):
                    result.append(ACTION.DOWN)
                yMovement -= yScale[0]
            else:
                result.append(ACTION.STAY)
    return result

def converter2(originalDim:coordObject,targetDim:coordObject,moves:list[ACTION]):
    """
    """
    xRatio = targetDim.x / originalDim.x # < 1 
    yRatio = targetDim.y / originalDim.y

    xMovement = 0
    yMovement = 0
    result:list[ACTION] = []
    for move in moves:
        xMovement +=xDelta(move) * xRatio
        yMovement +=yDelta(move) * yRatio
        if xMovement >= 1:
            if yMovement >= 1:
                result.append(ACTION.DIAG_UP_RIGHT)
                xMovement -= 1
                yMovement -= 1
            elif yMovement <= -1:
                result.append(ACTION.DIAG_DOWN_RIGHT)
                xMovement -= 1
                yMovement += 1
            else:
                xMovement -= 1
                result.append(ACTION.RIGHT)
        elif xMovement <= -1:
            if yMovement >= 1:
                result.append(ACTION.DIAG_UP_LEFT)
                xMovement += 1
                yMovement -= 1
            elif yMovement <= -1:
                result.append(ACTION.DIAG_DOWN_LEFT)
                xMovement += 1
                yMovement += 1
            else:
                xMovement += 1
                result.append(ACTION.LEFT)
        if yMovement >= 1:
            yMovement -= 1
            result.append(ACTION.UP)
        elif yMovement <= -1:
            yMovement += 1
            result.append(ACTION.DOWN)
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

def resizeRoute(name:str) -> list[list[ACTION]]:
    moves = readFileAction(name)
    return list(map(lambda r:converter2(BIGDIM,DIM,r),moves))

if __name__ == "__main__":
    originalDim = coordObject(4,4)
    targetDim = coordObject(2,2)
    moves = [ACTION.UP,ACTION.UP,ACTION.RIGHT,ACTION.RIGHT,ACTION.LEFT,ACTION.DIAG_UP_LEFT,ACTION.DOWN,ACTION.RIGHT,ACTION.UP,ACTION.DOWN]
    print(converter2(originalDim,targetDim,moves))