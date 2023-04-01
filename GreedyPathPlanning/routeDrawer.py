import matplotlib.pyplot as plt
from coordObject import coordObject
from constants import ACTION, BIGDIM, DIM, PAUSE_TIME, OBSTACLES, POIS, colors, markers
from POI import POI
from utils import readFileAction, flatten_obstacles, xDelta, yDelta, getListOfPois
from Obstacle import Obstacle


def calculateOffset(index):
    """
    Returns an offset for shifting an annotation when representing a UAV executing ACTION.STAY
    """
    result = coordObject(0, 0)
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


def drawRoute(dimensions: coordObject, Pois: list[POI], origin: coordObject, routes: list[list[ACTION]]):
    """
    Graphs using pyplot the trajectories of each UAV, in the order of the routes.
    """
    plt.figure()
    plt.xlim(-0.3, dimensions.x+0.3)
    plt.ylim(-0.3, dimensions.y+0.3)
    plt.grid(True)

    for poi in Pois:
        x = poi.getSection(dimensions).x
        y = poi.getSection(dimensions).y
        plt.plot(x, y, marker='o', color='k')

    for index, route in enumerate(routes):
        position = coordObject(origin.x, origin.y)
        xCoordenates = []
        yCoordenates = []
        offset = calculateOffset(index)
        for moveIndex, move in enumerate(route):
            xCoordenates.append(position.x)
            yCoordenates.append(position.y)
            position.x += xDelta(move)
            position.y += yDelta(move)
            tempPos = plt.scatter(position.x, position.y,
                                  marker=markers[index], color=colors[index])
            if move == ACTION.STAY:
                plt.scatter(position.x, position.y, s=80,
                            facecolors='none', edgecolors=colors[index])
                if moveIndex == 0 or route[moveIndex-1] != ACTION.STAY:
                    acc = 1
                    i = 1
                    while moveIndex+i in range(len(route)) and route[moveIndex + i] == ACTION.STAY:
                        acc += 1
                        i += 1
                    plt.annotate(acc, (position.x+offset.x,
                                 position.y+offset.y), color=colors[index])
            plt.plot(xCoordenates, yCoordenates, color=colors[index])
            plt.pause(PAUSE_TIME)
            tempPos.remove()
        xCoordenates.append(position.x)
        yCoordenates.append(position.y)
        plt.plot(xCoordenates, yCoordenates, color=colors[index])
    plt.show()
    return 0


def drawRouteAlt(dimensions: coordObject, Pois: list[POI], origin: coordObject, obstacles: list[Obstacle], routes: list[list[ACTION]]):
    """
    Graphs using pyplot the trajectories of the UAVs, graphins simultaneosly each move of each drone
    """
    plt.figure()
    plt.xlim(-0.3, dimensions.x + 0.3)
    plt.ylim(-0.3, dimensions.y + 0.3)
    plt.grid(True)
    ticks = [t for t in range(dimensions.x)]
    plt.xticks(ticks=ticks)
    plt.yticks(ticks=ticks)
    for badSection in flatten_obstacles(dimensions):
        plt.fill([badSection.x, badSection.x+1, badSection.x+1, badSection.x],
                 [badSection.y, badSection.y, badSection.y+1, badSection.y+1],
                 color='black', alpha=0.5)

    for poi in Pois:
        x = poi.getSection(dimensions).x + 0.5
        y = poi.getSection(dimensions).y + 0.5
        plt.plot(x, y, marker='o', color='k')

    positions = [coordObject(origin.x + 0.5, origin.y + 0.5) for _ in routes]
    time = max(map(len, routes))
    moveStart = coordObject(origin.x, origin.y)
    moveEnd = coordObject(origin.x, origin.y)
    tempPos = []
    for t in range(time):
        for index, route in enumerate(routes):
            offset = calculateOffset(index)
            if t < len(route):
                move = route[t]
                moveStart.x = positions[index].x
                moveStart.y = positions[index].y
                moveEnd.x = moveStart.x + xDelta(move)
                moveEnd.y = moveStart.y + yDelta(move)
                positions[index].x = moveEnd.x
                positions[index].y = moveEnd.y
                tempPos.append(plt.scatter(
                    moveEnd.x, moveEnd.y, marker=markers[0], color=colors[index], s=100))
                if move == ACTION.STAY:
                    plt.scatter(moveEnd.x, moveEnd.y, s=80,
                                facecolors='none', edgecolors=colors[index])
                    if t == 0 or t not in range(len(route)) or route[t-1] != ACTION.STAY:
                        acc = 1
                        i = 1
                        while t+i in range(len(route)) and route[t + i] == ACTION.STAY:
                            acc += 1
                            i += 1
                        plt.annotate(acc, (moveEnd.x+offset.x,
                                     moveEnd.y+offset.y), color=colors[index])
                plt.plot([moveStart.x, moveEnd.x], [
                         moveStart.y, moveEnd.y], color=colors[index])

        timer = plt.annotate(
            str(t), [dimensions.x + 0.3, dimensions.y + 0.3], fontsize=22)
        if(PAUSE_TIME > 0):
            plt.pause(PAUSE_TIME)
        for temp in tempPos:
            temp.remove()
        tempPos.clear()
        timer.remove()
    timer = plt.annotate(
        str(t+1), [dimensions.x + 0.3, dimensions.y + 0.3], fontsize=22)
    plt.show()


def interpretFile(name: str, poi: list[POI] = getListOfPois(), dimensions: coordObject = BIGDIM, origin: coordObject = coordObject(0, 0), obstacles: list[Obstacle] = OBSTACLES):
    routes = readFileAction(name)
    drawRouteAlt(dimensions, poi, origin, obstacles, routes)

# given a list of lists of strings, returns a list of ACTIONS


def parseMoves(listOfLists: list[list[str]]) -> list[ACTION]:
    res = []
    for line in listOfLists:
        res.append(list(map(lambda x: ACTION(x), line)))
    return res


def mapFun(coord: coordObject):
    return POI(coord, 0, 0)


if __name__ == '__main__':
    poiList = []
    # for each POI create a POI
    for poi in POIS:
        poiList.append(POI(poi, 0, 0))

    interpretFile('9.txt', poiList, DIM, coordObject(0, 0), OBSTACLES)
