from sys import argv
from constants import DIM
from coordObject import coordObject
from dimConverter import resizeRoute
from routeDrawer import drawRouteAlt, interpretFile
from pathGenerator import runGreedy
from POI import POI


if __name__ == "__main__":
    # try:
    #     if (int(argv[1]) == 0):
    #         for k in range(70, 100):
    #             for i in range(1, 10):
    #                 runGreedy(i, k/100)
    #     elif (int(argv[1]) == 1):
    #         interpretFile('1.txt')
    #     elif (int(argv[1]) == 2):
    #         POIPosition = list([coordObject(0.3, 0.3), coordObject(0.8, 0.8)])
    #         POITimes = [2, 5]
    #         POIList: list[POI] = []
    #         for i in range(len(POIPosition)):
    #             currPOI = POI(POIPosition[i], POITimes[i], i)
    #             POIList.append(currPOI)
    #         newRoutes = resizeRoute('1.txt')
    #         drawRouteAlt(DIM, POIList, coordObject(0, 0), [], newRoutes)
    #     else:
    #         print("Invalid operation")
    #         print("Valid operations are ")
    # except IndexError as err:
    #     print('An operation argument is needed')
    #     for k in range(70, 100):
    #         for i in range(1, 10):
    #             runGreedy(i, k/100)
    runGreedy(1, 90/100)