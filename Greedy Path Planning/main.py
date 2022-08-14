from sys import argv
from constants import DIM
from coordObject import coordObject
from dimConverter import resizeRoute
from routeDrawer import drawRouteAlt, interpretFile
from pathGenerator import runGreedy
from evaluator import evaluateOutputs
from POI import POI
import argparse

parser = argparse.ArgumentParser()


if __name__ == "__main__":
    try:
        parser.add_argument('-t', '--task', help='task',
                            type=str, default='create')
        parser.add_argument(
            "-f", "--file", help="File to interpret", dest="file", type=str)
        args = parser.parse_args()
        # Create dataset
        if (args.task == 'create'):
            # runGreedy(1,90/100)
            for k in range(70, 100):
                for i in range(1, 10):
                    runGreedy(i, k/100)
        # Print UAVs flight
        elif (args.task == 'print'):
            interpretFile(args.file, dimensions=DIM)
        elif (int(argv[1]) == 2):
            POIPosition = list([coordObject(0.3, 0.3), coordObject(0.8, 0.8)])
            POITimes = [2, 5]
            POIList: list[POI] = []
            for i in range(len(POIPosition)):
                currPOI = POI(POIPosition[i], POITimes[i], i)
                POIList.append(currPOI)
            newRoutes = resizeRoute('1.txt')
            drawRouteAlt(DIM, POIList, coordObject(0, 0), [], newRoutes)
        elif(int(argv[1]) == 3):
            evaluateOutputs()
        else:
            print("Invalid operation")
            print("Valid operations are ")
    except IndexError as err:
        print(
            err.with_traceback(err))
