import matplotlib.pyplot as plt
from coordObject import coordObject
from constants import ACTION
from POI import POI

colors = ['b','g','r','c','m','k']
markers = ['o','^','v']

def calculateOffset(index):
    result = coordObject(0,0)
    if(index % 4 == 0):
        result.x = 0.1
        result.y = 0.1
    elif(index % 4 == 1):
        result.x = 0.1
        result.y = -0.2
    elif(index % 4 == 2):
        result.x = -0.1
        result.y = -0.2
    else:
        result.x = -0.1
        result.y = 0.1
    return result
    

def drawRoute(dimensions:coordObject, Pois:list[POI], origin:coordObject, routes:list[list[ACTION]]):
  plt.figure()
  plt.xlim(-0.3,dimensions.x+0.3)
  plt.ylim(-0.3,dimensions.y+0.3)
  plt.grid(True)

  for poi in Pois:
      x = poi.getSection(dimensions).x
      y = poi.getSection(dimensions).y
      plt.plot(x,y,marker='o',color='k')

  for index,route in enumerate(routes):
    position = coordObject(origin.x,origin.y)
    xCoordenates = []
    yCoordenates = []
    offset = calculateOffset(index)
    for moveIndex,move in enumerate(route):
        xCoordenates.append(position.x)
        yCoordenates.append(position.y)
        position.x += xDelta(move)
        position.y += yDelta(move)
        tempPos = plt.scatter(position.x,position.y,marker=markers[index],color=colors[index])
        if move == ACTION.STAY:
            plt.scatter(position.x,position.y,s=80,facecolors='none',edgecolors=colors[index])
            if  moveIndex ==0 or route[moveIndex-1] != ACTION.STAY:
                acc = 1
                i = 1
                while route[moveIndex + i] == ACTION.STAY:
                    acc += 1
                    i += 1
                plt.annotate(acc,(position.x+offset.x,position.y+offset.y),color=colors[index])
        plt.plot(xCoordenates,yCoordenates,color=colors[index])
        plt.pause(1)
        tempPos.remove()
    xCoordenates.append(position.x)
    yCoordenates.append(position.y)
    plt.plot(xCoordenates,yCoordenates,color=colors[index])
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

def mapFun(coord:coordObject):
    return POI(coord,0,0)

if __name__ == '__main__':
    routes = [[ACTION.UP,ACTION.STAY,ACTION.STAY,ACTION.RIGHT,ACTION.RIGHT,ACTION.DOWN,ACTION.RIGHT,ACTION.STAY,ACTION.DIAG_UP_RIGHT],[ACTION.UP,ACTION.STAY,ACTION.RIGHT,ACTION.UP,ACTION.UP]]
    coordPoi = [coordObject(0.8,0.5),coordObject(0.75,0.9),coordObject(0.9,0)]
    poi = list(map(mapFun,coordPoi))
    dimensions = coordObject(5,5)
    origin = coordObject(0,0)
    drawRoute(dimensions,poi,origin,routes)