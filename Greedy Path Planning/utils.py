from classes import *
from constants import *


def printMapGrid(dronePos:coordObject, POIPos):
    for aux in range(DIM.y):
        if aux == 0:
            for x in range(DIM.x):
                print('_______', end='')
        print()
        print()
        print('|    ', end='')
        # to print it in right order
        y = DIM.y - aux -1
        for x in range(DIM.x):
            isPOI = [coords for coords in POIPos if (coords.x == x and coords.y == y)] != []
            isDrone = x == dronePos.x and y == dronePos.y
            if(isDrone):
                print('D',end='')
            if(isPOI):
                print('P',end='')
            if(not isPOI and not isDrone):
                print('-',end='')
            # prints a tab
            print('    ',end='')
        print('|', end='')
        print('')
        if aux+1 == DIM.y:
            for x in range(DIM.x):
                print('_______', end='')
        print()
