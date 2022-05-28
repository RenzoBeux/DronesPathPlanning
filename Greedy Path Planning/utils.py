from constants import ACTION, DIM
from coordObject import coordObject
from POI import POI
from UAV import UAV
from heuristics.ImoveHeuristic import moveHeuristic
from heuristics.nefesto import heuristic_nefesto
def printMapGrid(drones: list[UAV], POIPos):
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
            filtered = list(filter(
                lambda drone: x == drone.position.x and y == drone.position.y, drones))
            isDrone = list(filtered) != []
            if(isDrone):
                for d in filtered:
                    print('D'+str(d.id), end='')
            if(isPOI):
                print('P', end='')
            if(not isPOI and not isDrone):
                print('-', end='')
            # prints a tab
            print('    ', end='')
        print('|', end='')
        print('')
        if aux+1 == DIM.y:
            for x in range(DIM.x):
                print('_______', end='')
        print()
