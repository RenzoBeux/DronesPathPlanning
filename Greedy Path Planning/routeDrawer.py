import matplotlib.pyplot as plt
from coordObject import coordObject
from constants import ACTION
from POI import POI
from utils import readFileAction

colors = ['b','g','r','c','m','k']
markers = ['o','^','v']

def calculateOffset(index):
    """
    Returns an offset for shifting an annotation when representing a UAV executing ACTION.STAY
    """
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
  """
  Graphs using pyplot the trajectories of each UAV, in the order of the routes.
  """
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
                while moveIndex+i in range(len(route)) and route[moveIndex + i] == ACTION.STAY:
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

def drawRouteAlt(dimensions:coordObject, Pois:list[POI], origin:coordObject, routes:list[list[ACTION]]):
    """
    Graphs using pyplot the trajectories of the UAVs, graphins simultaneosly each move of each drone
    """
    plt.figure()
    plt.xlim(-0.3,dimensions.x+0.3)
    plt.ylim(-0.3,dimensions.y+0.3)
    plt.grid(True)
    
    for poi in Pois:
        x = poi.getSection(dimensions).x + 0.5
        y = poi.getSection(dimensions).y + 0.5
        plt.plot(x,y,marker='o',color='k')

    positions = [coordObject(origin.x + 0.5,origin.y + 0.5) for _ in routes] 
    
    time = max(map(len,routes))
    moveStart = coordObject(origin.x,origin.y)
    moveEnd = coordObject(origin.x,origin.y)
    tempPos = []
    for t in range(time):
        for index,route in enumerate(routes):
            offset = calculateOffset(index)
            if t < len(route):
                move = route[t]
                moveStart.x = positions[index].x
                moveStart.y = positions[index].y
                moveEnd.x = moveStart.x + xDelta(move)
                moveEnd.y = moveStart.y + yDelta(move)
                positions[index].x = moveEnd.x
                positions[index].y = moveEnd.y
                tempPos.append(plt.scatter(moveEnd.x,moveEnd.y,marker=markers[index],color=colors[index],s=100))
                if move == ACTION.STAY:
                    plt.scatter(moveEnd.x,moveEnd.y,s=80,facecolors='none',edgecolors=colors[index])
                    if  t == 0 or t not in range(len(route)) or route[t-1] != ACTION.STAY:
                        acc = 1
                        i = 1
                        while t+i in range(len(route)) and route[t + i] == ACTION.STAY:
                            acc += 1
                            i += 1
                        plt.annotate(acc,(moveEnd.x+offset.x,moveEnd.y+offset.y),color=colors[index])
                plt.plot([moveStart.x,moveEnd.x],[moveStart.y,moveEnd.y],color=colors[index])

        plt.pause(0.2)
        for temp in tempPos:
            temp.remove()
        tempPos.clear()
    plt.show()

def xDelta(move:ACTION):
    """
    Calculates the shift an ACTION produces in the X axis
    """
    positives = [ACTION.DIAG_DOWN_RIGHT,ACTION.RIGHT,ACTION.DIAG_UP_RIGHT]
    negatives = [ACTION.DIAG_DOWN_LEFT,ACTION.LEFT, ACTION.DIAG_UP_LEFT]
    if move in positives:
        return 1
    elif move in negatives:
        return -1
    else:
        return 0

def yDelta(move:ACTION):
    """
    Calculates the shift an ACTION produces in the Y axis
    """
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

def interpretFile(name:str,poi:list[POI]=[],dimensions:coordObject=coordObject(5,5),origin:coordObject=coordObject(0,0)):
    routes = readFileAction(name)
    drawRouteAlt(dimensions,poi,origin,routes)

if __name__ == '__main__':
    routes = readFileAction('1.txt')
    coordPoi = [coordObject(0.8,0.5),coordObject(0.75,0.9),coordObject(0.9,0)]
    poi = list(map(mapFun,coordPoi))
    dimensions = coordObject(5,5)
    origin = coordObject(0,0)
    drawRouteAlt(dimensions,poi,origin,routes)