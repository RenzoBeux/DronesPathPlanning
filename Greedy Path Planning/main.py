from sys import argv
from constants import DIM
from coordObject import coordObject
from dimConverter import resizeRoute
from routeDrawer import drawRouteAlt, interpretFile
from pathGenerator import runGreedy


if __name__ == "__main__":
    try:
        if (int(argv[1]) == 0):
            for k in range(70,100):
                for i in range(1, 10):
                    runGreedy(i,k/100)
        elif (int(argv[1]) == 1):
            interpretFile('1.txt')
        elif (int(argv[1]) == 2):
            newRoutes = resizeRoute('1.txt')
            drawRouteAlt(DIM,[],coordObject(0,0),newRoutes)
        else:
            print("Invalid operation")
            print("Valid operations are ")
    except IndexError as err:
        print('An operation argument is needed')