import argparse
import traceback
from constants import DIM
from routeDrawer import interpretFile
from pathGenerator import runGreedy
from evaluator import evaluateFile
import os

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
            # creates folder output
            if not os.path.exists('output/'):
                os.makedirs('output/')
            # Now copy constants.py to output folder linux and windows
            if os.name == 'nt':
                os.system('copy constants.py output\\constants.py')
            else:
                os.system('cp constants.py output/constants.py')
                

            # runGreedy(1,90/100)
            for k in range(70, 100):
                for i in range(1, 100):
                    runGreedy(i, k/100)
        # Print UAVs flight
        elif (args.task == 'print'):
            interpretFile(args.file, dimensions=DIM)
        elif(args.task == 'evaluate'):
            print(evaluateFile(args.file))
        else:
            print("Invalid operation")
            print("Valid operations are ")
    except:
        traceback.print_exc()
