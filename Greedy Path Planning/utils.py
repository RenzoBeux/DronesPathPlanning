from POI import POI
from constants import ACTION, DIM, OBSTACLES
from UAV import UAV
from coordObject import coordObject


def printMapGrid(drones: list[UAV], POIPos: list[coordObject], obstacles: list[coordObject]):
    for aux in range(DIM.y):
        if aux == 0:
            for x in range(DIM.x):
                print('_______', end='')
        print()
        print()
        print('|    ', end='')
        # to print it in right order
        y = DIM.y - aux - 1
        for x in range(DIM.x):
            isPOI = [coords for coords in POIPos if (
                coords.x == x and coords.y == y)] != []
            isObstacle = [coords for coords in obstacles if (
                coords.x == x and coords.y == y)] != []
            filtered = list(filter(
                lambda drone: x == drone.position.x and y == drone.position.y, drones))
            isDrone = list(filtered) != []
            if(isDrone):
                for d in filtered:
                    print('D'+str(d.id), end='')
            if(isPOI):
                print('P', end='')
            if(isObstacle):
                print('O', end='')
            if(not isPOI and not isDrone and not isObstacle):
                print('-', end='')
            # prints a tab
            print('    ', end='')
        print('|', end='')
        print('')
        if aux+1 == DIM.y:
            for x in range(DIM.x):
                print('_______', end='')
        print()


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