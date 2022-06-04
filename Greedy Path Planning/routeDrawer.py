import matplotlib.pyplot as plt
from coordObject import coordObject
from constants import ACTION

def drawRoute(dim:coordObject, origin:coordObject, routes:list[list[ACTION]]):
  plt.figure()

  for route in routes:
    position = coordObject(origin.x,origin.y)
    xCoordenates = []
    yCoordenates = []
    for move in route:
        xCoordenates.append(position.x)
        yCoordenates.append(position.y)
        position.x += xDelta(move)
        position.y += yDelta(move)   
    xCoordenates.append(position.x)
    yCoordenates.append(position.y)
    plt.plot(xCoordenates,yCoordenates)
  plt.xlim(-0.3,dim.x+0.3)
  plt.ylim(-0.3,dim.y+0.3)
  plt.show()
  return 0


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

if __name__ == '__main__':
    routes = [[ACTION.UP,ACTION.RIGHT,ACTION.RIGHT,ACTION.DOWN,ACTION.RIGHT,ACTION.DIAG_UP_RIGHT],[ACTION.RIGHT]]
    dim = coordObject(5,5)
    origin = coordObject(0,0)
    drawRoute(dim,origin,routes)